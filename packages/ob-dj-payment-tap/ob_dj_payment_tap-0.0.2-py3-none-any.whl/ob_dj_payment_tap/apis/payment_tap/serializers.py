from rest_framework import serializers

from ob_dj_payment_tap.core.payment_tap.models import TapTransaction


class TapPaymentSerializer(serializers.Serializer):
    # read only
    id = serializers.IntegerField(label="ID", read_only=True)
    status = serializers.CharField(read_only=True)
    result = serializers.CharField(
        help_text="Status response from TAP gateway", max_length=100, read_only=True
    )
    payment_url = serializers.CharField(
        help_text="Captures generated URL for user payment",
        max_length=250,
        read_only=True,
    )
    charge_id = serializers.CharField(
        help_text="Charge ID returned from TAP", max_length=250, read_only=True
    )
    init_response = serializers.JSONField(allow_null=True, read_only=True)
    callback_response = serializers.JSONField(allow_null=True, read_only=True)

    # write only
    amount = serializers.DecimalField(decimal_places=3, max_digits=20, min_value=1)
    # TODO: Remove the default KWD currency code
    currency_code = serializers.CharField(max_length=5, default="KWD", required=False)
    created_at = serializers.DateTimeField(read_only=True)
    source = serializers.ChoiceField(
        choices=TapTransaction.Sources.choices, write_only=True
    )

    def create(self, validated_data):
        source = validated_data.get("source")
        amount = validated_data.get("amount")
        return TapTransaction.objects.create(
            user=self.context.get("request").user, source=source, amount=amount,
        )
