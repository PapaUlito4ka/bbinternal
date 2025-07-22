from django.db import models
import uuid
from accounts.models import Account


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_account = models.ForeignKey(
        Account, related_name="outgoing_transactions", on_delete=models.CASCADE
    )
    to_account = models.ForeignKey(
        Account, related_name="incoming_transactions", on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} from {self.from_account.owner_name} to {self.to_account.owner_name}"
