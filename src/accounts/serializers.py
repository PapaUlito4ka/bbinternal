from rest_framework import serializers
from accounts.models import Account
from transactions.serializers import TransactionSerializer


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "owner_name", "balance", "created_at"]
        read_only_fields = ["id", "balance", "created_at"]


class AccountWithTransactionsSerializer(serializers.ModelSerializer):
    outgoing_transactions = TransactionSerializer(many=True, read_only=True)
    incoming_transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = [
            "id",
            "owner_name",
            "balance",
            "created_at",
            "outgoing_transactions",
            "incoming_transactions",
        ]
