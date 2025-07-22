from decimal import Decimal

from rest_framework.exceptions import ValidationError

from transactions.models import Transaction
from accounts.models import Account
from django.db import transaction as db_transaction


class TransactionService:
    @staticmethod
    def create_transaction(
        from_account: Account, to_account: Account, amount: Decimal
    ) -> Transaction:
        with db_transaction.atomic():
            from_account = Account.objects.select_for_update().get(id=from_account.id)
            to_account = Account.objects.select_for_update().get(id=to_account.id)

            if from_account.id == to_account.id:
                raise ValidationError("Cannot transfer to the same account.")

            if amount <= Decimal("0"):
                raise ValidationError("Amount must be positive.")

            if from_account.balance < amount:
                raise ValidationError("Insufficient funds.")

            from_account.balance -= amount
            to_account.balance += amount

            from_account.save()
            to_account.save()

            transaction = Transaction.objects.create(
                from_account=from_account, to_account=to_account, amount=amount
            )

            return transaction
