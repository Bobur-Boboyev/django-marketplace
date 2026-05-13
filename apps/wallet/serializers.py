from rest_framework import serializers

from .models import WalletTransaction


class WithdrawalRequestSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    card_number = serializers.CharField(max_length=32)

    def validate_amount(self, value):

        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")

        return value

    def validate_card_number(self, value):

        if len(value) < 16:
            raise serializers.ValidationError("Invalid card number")

        return value


class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction

        fields = [
            "id",
            "amount",
            "type",
            "reference",
            "created_at",
        ]
