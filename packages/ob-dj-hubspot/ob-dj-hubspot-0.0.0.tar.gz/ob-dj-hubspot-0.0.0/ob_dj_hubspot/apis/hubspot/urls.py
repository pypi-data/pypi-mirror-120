from django.urls import path

from ob_dj_hubspot.apis.hubspot.views import CallBackView

app_name = "hubspot"

urlpatterns = [
    path("", CallBackView.as_view(), name="callback",),
]
