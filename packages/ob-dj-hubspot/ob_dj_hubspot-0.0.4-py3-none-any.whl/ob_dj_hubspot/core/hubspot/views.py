import logging

import requests
from celery import current_app
from django.conf import settings
from django.contrib.sites.models import Site
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from ob_dj_hubspot.core.hubspot.models import HSOAuth

logger = logging.getLogger(__name__)


class HubSpotOAuthView(View):
    permissions: tuple = ("hubspot.add_oauth",)

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if "code" not in request.GET:
            raise Http404
        code = request.GET.get("code")

        site = Site.objects.get_current()

        response = requests.post(
            url=f"{settings.HS_API_BASE_URL}/oauth/v1/token",
            data={
                "grant_type": "authorization_code",
                "client_id": settings.HS_CLIENT_ID,
                "client_secret": settings.HS_CLIENT_SECRET,
                "redirect_uri": settings.HS_REDIRECT_URI,
                "code": code,
            },
        )
        response.raise_for_status()
        logger.debug(
            f"{self.__class__.__name__}() Response "
            f"<url:{response.url}, "
            f"status_code:{response.status_code}>"
        )
        _r = response.json()

        try:
            hs_oa = HSOAuth.objects.get(site=site)
            hs_oa.access_token = _r.get("access_token")
            hs_oa.refresh_token = _r.get("refresh_token")
            hs_oa.expires_in = _r.get("expires_in")
            hs_oa.save()
        except HSOAuth.DoesNotExist:
            hs_oa = HSOAuth.objects.create(
                site=site,
                access_token=_r.get("access_token"),
                refresh_token=_r.get("refresh_token"),
                expires_in=_r.get("expires_in"),
            )

        # TODO: Post message in sessions to show success in admin
        #       messages https://docs.djangoproject.com/en/3.1/ref/contrib/messages/
        return redirect(reverse("admin:hubspot_hsoauth_change", args=[hs_oa.id,]))


class HubSpotSyncAllView(View):
    """ HubSpotSyncAllView represent an html view available only for system superusers to
    refresh data from hubspot and re-sync contacts, companies and associations.
    """

    permissions: tuple = ("integrations.add_oauth",)

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        site = Site.objects.get_current()

        instance = HSOAuth.objects.get(site=site)
        current_app.send_task(
            "ob_dj_hubspot.core.hubspot.tasks.hs_sync_all_objects_contacts",
        )

        return redirect(reverse("admin:hubspot_hsoauth_change", args=[instance.id,]))
