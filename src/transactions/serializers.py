from rest_framework import serializers
from transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "from_account", "to_account", "amount", "created_at"]
        read_only_fields = ["id", "created_at"]
