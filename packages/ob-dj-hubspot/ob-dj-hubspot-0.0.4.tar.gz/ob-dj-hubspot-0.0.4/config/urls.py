from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"hubspot/", include("ob_dj_hubspot.apis.hubspot.urls", namespace="hubspot"),),
]
