from django.urls import path

from ob_dj_hubspot.core.hubspot import views
from ob_dj_hubspot.core.hubspot.utils import django_admin_staff_permission_required

app_name = "hubspot-admin"

urlpatterns = [
    path(
        "oauth",
        django_admin_staff_permission_required(views.HubSpotOAuthView.permissions)(
            views.HubSpotOAuthView.as_view()
        ),
        name="oauth",
    ),
    path(
        "sync-all",
        django_admin_staff_permission_required(views.HubSpotSyncAllView.permissions)(
            views.HubSpotSyncAllView.as_view()
        ),
        name="sync_all",
    ),
]
