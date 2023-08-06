import typing

from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django_cryptography.fields import encrypt

from ob_dj_hubspot.core.hubspot.managers import (
    HSCompanyManager,
    HSContactManager,
    HSDealManager,
    HSOAuthManager,
)
from ob_dj_hubspot.core.hubspot.signals import (
    company_deleted,
    company_updated,
    contact_deleted,
    contact_updated,
    deal_deleted,
    deal_updated,
)


class HSOAuth(models.Model):
    """ HSOAuth is a represent stored information of hubspot
    """

    site = models.OneToOneField(Site, on_delete=models.CASCADE, related_name="hs_oa")
    refresh_token = encrypt(models.CharField(max_length=3000))
    access_token = encrypt(models.CharField(max_length=3000))
    expires_in = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    stale = models.BooleanField(default=False)

    objects = HSOAuthManager()

    class Meta:
        verbose_name = _("HubSpot: OAuth")
        verbose_name_plural = _("HubSpot: OAuth")

    def __str__(self) -> typing.Text:
        return f"<{self._meta.object_name} Pk={self.pk}>"

    def save(self, **kwargs) -> None:
        if not self.pk:
            try:
                if self.site:
                    pass
            except ObjectDoesNotExist:
                self.site = Site.objects.get_current()
        super().save(**kwargs)


class HSContact(models.Model):
    """ HSContact is a represent stored information from hubspot

    Note: the data will be synced on authorization and will update via webhooks
    """

    oauth = models.ForeignKey(HSOAuth, on_delete=models.CASCADE)
    contact_id = models.CharField(max_length=3000, unique=True)
    properties = models.JSONField()
    associations = models.JSONField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    objects = HSContactManager()

    class Meta:
        verbose_name = _("HubSpot: Contact")
        verbose_name_plural = _("HubSpot: Contacts")

    def __str__(self) -> typing.Text:
        return f"{self.email}"

    @property
    def email(self):
        if "email" in self.properties:
            return self.properties.get("email")

    @property
    def full_name(self):
        if "firstname" in self.properties or "lastname" in self.properties:
            return (
                f"{self.properties.get('firstname')} {self.properties.get('lastname')}"
            )

    def mark_deleted(self) -> typing.NoReturn:
        self.deleted_at = now()
        self.save()
        contact_deleted.send(sender=self.__class__, instance=self)

    def save_properties(self, key, value) -> typing.NoReturn:
        self.properties[key] = value
        contact_updated.send(
            sender=self.__class__, instance=self, property_key=key, property_value=value
        )
        self.save()


class HSCompany(models.Model):
    """ HSCompany is a represent stored information of hubspot

    Note: the data will be synced on authorization and will update via webhooks
    """

    oauth = models.ForeignKey(HSOAuth, on_delete=models.CASCADE)
    company_id = models.CharField(max_length=3000, unique=True)
    properties = models.JSONField()
    associations = models.JSONField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    objects = HSCompanyManager()

    class Meta:
        verbose_name = _("HubSpot: Company")
        verbose_name_plural = _("HubSpot: Companies")

    def __str__(self) -> typing.Text:
        return f"{self.name}"

    @property
    def name(self):
        if "name" in self.properties:
            return self.properties.get("name")

    @property
    def domain(self):
        if "domain" in self.properties:
            return self.properties.get("domain")

    def mark_deleted(self) -> typing.NoReturn:
        self.deleted_at = now()
        self.save()
        company_deleted.send(sender=self.__class__, instance=self)

    def save_properties(self, key, value) -> typing.NoReturn:
        self.properties[key] = value
        company_updated.send(
            sender=self.__class__, instance=self, property_key=key, property_value=value
        )
        self.save()


class HSDeal(models.Model):
    """ HSDeal is a represent stored information of hubspot

    Note: the data will be synced on authorization and will update via webhooks
    """

    oauth = models.ForeignKey(HSOAuth, on_delete=models.CASCADE, related_name="hs_oa")
    deal_id = models.CharField(max_length=3000, unique=True)
    properties = models.JSONField(default=dict, null=True, blank=True)
    associations = models.JSONField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    objects = HSDealManager()

    class Meta:
        verbose_name = _("HubSpot: Deal")
        verbose_name_plural = _("HubSpot: Deals")

    def __str__(self) -> typing.Text:
        return f"<{self._meta.object_name} Pk={self.pk}>"

    @property
    def amount(self):
        if "amount" in self.properties:
            return self.properties.get("amount")

    @property
    def deal_name(self):
        if "dealname" in self.properties:
            return self.properties.get("dealname")

    @property
    def pipeline(self):
        if "pipeline" in self.properties:
            return self.properties.get("pipeline")

    def mark_deleted(self) -> typing.NoReturn:
        self.deleted_at = now()
        self.save()
        deal_deleted.send(sender=self.__class__, instance=self)

    def save_properties(self, key, value) -> typing.NoReturn:
        self.properties[key] = value
        deal_updated.send(
            sender=self.__class__, instance=self, property_key=key, property_value=value
        )
        self.save()
