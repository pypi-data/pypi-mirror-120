from django.apps import apps
from django.contrib import admin
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html

from ob_dj_hubspot.core.hubspot.models import HSCompany, HSContact, HSDeal, HSOAuth


class HSOAuthAdmin(admin.ModelAdmin,):
    model = HSOAuth
    list_display = ("site", "expires_in", "hs_action")
    change_list_template = "admin_oauth_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("add-oauth/", self.add_oauth),
        ]
        return my_urls + urls

    def add_oauth(self, request):
        return HttpResponseRedirect(self.hs_oauth_link())

    @staticmethod
    def hs_oauth_link() -> str:
        return apps.get_app_config("hubspot").get_oauth_link()

    def hs_action(self, obj):
        if obj.hs_oa:
            pass
        return format_html(
            '<a class="button" href="{}">Sync Data</a> '
            '<a class="button" href="{}">Refresh Tokens</a>',
            reverse("hubspot-admin:sync_all"),
            apps.get_app_config("hubspot").get_oauth_link(),
        )

    hs_action.short_description = "HubSpot OAuth"
    hs_action.allow_tags = True

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False


class HSOContactAdmin(admin.ModelAdmin,):
    model = HSContact
    list_display = ("contact_id", "email")


class HSOCompanyAdmin(admin.ModelAdmin,):
    model = HSCompany
    list_display = ("company_id", "name", "domain")


class HSDealAdmin(admin.ModelAdmin,):
    model = HSDeal
    list_display = ("deal_id", "deal_name", "pipeline", "amount")


admin.site.register(HSOAuth, HSOAuthAdmin)
admin.site.register(HSContact, HSOContactAdmin)
admin.site.register(HSCompany, HSOCompanyAdmin)
admin.site.register(HSDeal, HSDealAdmin)
