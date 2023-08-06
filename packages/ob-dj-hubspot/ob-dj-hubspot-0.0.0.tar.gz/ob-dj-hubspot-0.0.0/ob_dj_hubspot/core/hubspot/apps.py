from urllib.parse import urlencode

from django.apps import AppConfig
from django.conf import settings
from django.core.checks import register
from django.utils.translation import gettext_lazy as _

from ob_dj_hubspot.core.hubspot import settings_validation


class HubSpotConfig(AppConfig):
    name = "ob_dj_hubspot.core.hubspot"
    verbose_name = _("HubSpot")

    @staticmethod
    def get_oauth_link():
        params = {
            "client_id": settings.HS_CLIENT_ID,
            "redirect_uri": settings.HS_REDIRECT_URI,
            "scope": settings.HS_SCOPES,
        }
        return f"https://app.hubspot.com/oauth/authorize?{urlencode(params)}"

    def ready(self):
        register(settings_validation.required_settings)
        register(settings_validation.required_dependencies)
        register(settings_validation.required_installed_apps)
