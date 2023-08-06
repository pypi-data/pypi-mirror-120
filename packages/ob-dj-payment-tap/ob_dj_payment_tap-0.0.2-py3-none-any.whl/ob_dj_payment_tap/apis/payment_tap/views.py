import logging
import os
import time
import typing

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from ob_dj_payment_tap.apis.payment_tap.serializers import TapPaymentSerializer
from ob_dj_payment_tap.core.payment_tap.models import TapTransaction
from ob_dj_payment_tap.core.payment_tap.utils import TapChallengeException

logger = logging.getLogger(__name__)


@method_decorator(
    name="callback",
    decorator=swagger_auto_schema(
        operation_summary="gateway_tap callback",
        operation_description="""
            - gateway_tap callback,
            """,
        tags=["Payment (Tap)"],
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_summary="Create Payment (using TAP)",
        operation_description="""
                      """,
        tags=["Payment (Tap)"],
    ),
)
@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_summary="Retrieve Tap Transaction",
        operation_description="""
            Retrieve Tap Transaction from charge id
            """,
        tags=["Billing"],
    ),
)
class TapPaymentViewSet(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    http_method_names = ["get", "post"]
    queryset = TapTransaction.objects.all()
    serializer_class = TapPaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    # TODO: Add custom permission for validating TAP Call backs
    @action(detail=False, methods=["POST"], permission_classes=[permissions.AllowAny])
    def callback(self, request) -> typing.Any:
        tap_response = request.data
        try:
            tap_filter = {"charge_id": tap_response["id"]}
        except KeyError:
            raise ValidationError(_("charge_id attribute is required"))

        try:
            logger.debug(f"Received callback with payload {tap_response}")
            instance = TapTransaction.objects.get(**tap_filter)
            instance.update_from_payload(payload=tap_response)
        except ObjectDoesNotExist:
            logger.warning(
                f"Callback received from TAP with ID: {tap_filter.__str__()} not found"
            )
            return HttpResponseNotFound("Wrong charge Id")

        return Response({"success": True}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], permission_classes=[permissions.AllowAny])
    def get(self, request, *args, **kwargs):
        charge_id = request.query_params.get("tap_id")
        challenge = request.query_params.get("challenge")
        if not charge_id or not challenge:
            raise ValidationError(_("tap_id and challenge required in params."))

        logger.info(
            f"Retrieving Tap Transaction with charge_id {charge_id} and challenge {challenge}"
        )
        # Requests return from Tap with delay, a while loop with break timeout
        # to query locally for the response if ObjectDoesNotExist returned
        timeout = 15  # [seconds]
        timeout_start = time.time()
        while True:
            delta = time.time() - timeout_start
            try:
                instance = TapTransaction.objects.get(charge_id=charge_id)
                instance.validate_challenge(data=challenge, raise_exception=True)
                break
            except ObjectDoesNotExist:
                # IMPORTANT: "PYTEST_CURRENT_TEST" in os.environ so
                #            the condition is skipped in unit testing only
                if delta >= timeout or "PYTEST_CURRENT_TEST" in os.environ:
                    return HttpResponseNotFound("Wrong charge Id")
            except TapChallengeException:
                return Response("Invalid challenge", status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
