import hashlib
import logging

from django.conf import settings
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ob_dj_hubspot.apis.hubspot.utils import HubSpotCallbackProcessor

logger = logging.getLogger(__name__)


class CallBackView(APIView):
    permission_classes = [
        permissions.AllowAny,
    ]
    allowed_methods = [
        "POST",
    ]

    def post(self, request) -> Response:
        hs_signature = request.headers.get("X-HubSpot-Signature")
        logger.debug(
            "Signature hashing for hubspot \n"
            f"Absolute URI {request.build_absolute_uri()} \n"
            f"Method {request.method} \n"
            f"HS Client Secret {settings.HS_CLIENT_SECRET} \n"
        )
        signature = (
            settings.HS_CLIENT_SECRET.encode("utf-8")
            + request.method.encode("utf-8")
            + request.build_absolute_uri().encode("utf-8")
            + request.body
        )
        signature = hashlib.sha256(signature).hexdigest()
        logger.debug(
            "Evaluating HubSpot Hash \n"
            f"HS Hash: {hs_signature} \n"
            f"Computed Hash: {signature} \n"
        )

        # TODO: Hash verification not working :/
        # if not signature == hs_signature:
        #     return Response(status=status.HTTP_403_FORBIDDEN)
        # TODO: Replace with Celery Task to asyncly process the payload
        for event in request.data:
            handler = HubSpotCallbackProcessor(payload=event)
            handler.process()
        return Response(status=status.HTTP_200_OK)
