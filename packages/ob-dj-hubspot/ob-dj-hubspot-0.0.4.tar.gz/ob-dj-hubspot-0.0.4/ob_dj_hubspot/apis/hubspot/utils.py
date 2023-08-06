import logging
import typing

from django.core.exceptions import ObjectDoesNotExist

from ob_dj_hubspot.core.hubspot.models import HSCompany, HSContact, HSDeal

logger = logging.getLogger(__name__)


def camel_to_snake(s: typing.Text) -> typing.Text:
    return "".join(["_" + c.lower() if c.isupper() else c for c in s]).lstrip("_")


class HubSpotCallbackProcessor(object):
    def __init__(self, payload: typing.Dict):
        self.payload = payload
        model, self.subscription_type = self.payload.get("subscriptionType").split(".")
        self.subscription_type = f"object__{camel_to_snake(self.subscription_type)}"
        if model == "contact":
            self.model = HSContact
        if model == "deal":
            self.model = HSDeal
        if model == "company":
            self.model = HSCompany

    def process(self) -> typing.NoReturn:
        return getattr(self, self.subscription_type)()

    def object__deletion(self) -> typing.NoReturn:
        try:
            model = self.model
            logger.debug(
                "HubSpot Callback Processor (object__deletion): Processing with payload \n"
                f"{self.payload}"
            )
            instance = model.objects.get_by_object_id(
                object_id=self.payload.get("objectId"),
            )
            instance.mark_deleted()
            logger.debug(
                f"HubSpot Callback Processor (object__deletion): mark deal ({instance.id}) as deleted"
            )
        except ObjectDoesNotExist:
            logger.debug(
                f"HubSpot Callback Processor (object__deletion): Error cannot find deal objectId"
            )

    def object__creation(self):
        try:
            model = self.model
            logger.debug(
                "HubSpot Callback Processor (object__creation): Processing with payload \n"
                f"{self.payload}"
            )
            instance = model.objects.get_by_object_id(
                object_id=self.payload.get("objectId"),
            )
            logger.debug(
                f"HubSpot Callback Processor (object__creation): Already processed with id ({instance.id})"
            )
        except ObjectDoesNotExist:
            instance = model.objects.create_by_object_id(
                object_id=self.payload.get("objectId"), properties={}
            )
            logger.debug(
                f"HubSpot Callback Processor (object__creation): Processed deal id ({instance.id})"
            )

    def object__property_change(self) -> typing.NoReturn:
        try:
            model = self.model
            logger.debug(
                "HubSpot Callback Processor (object__property_change): Processing with payload \n"
                f"{self.payload}"
            )
            contact = model.objects.get_by_object_id(
                object_id=self.payload.get("objectId")
            )
            property_name = self.payload.get("propertyName")
            property_value = self.payload.get("propertyValue")
            contact.save_properties(key=property_name, value=property_value)
            logger.debug(
                f"HubSpot Callback Processor (object__property_change): "
                f"<propertyName: {property_name}>"
                f"<propertyValue: {property_value}>"
            )
        except ObjectDoesNotExist:
            logger.warning(
                f"HubSpot Callback Processor (object__property_change): "
                f"failed cannot find objectId: {self.payload.get('objectId')}"
            )
