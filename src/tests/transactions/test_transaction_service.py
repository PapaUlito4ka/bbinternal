import pytest
from decimal import Decimal

from rest_framework.exceptions import ValidationError

from accounts.models import Account
from transactions.services import TransactionService


@pytest.fixture
def accounts():
    sender = Account.objects.create(owner_name="Artem", balance=Decimal("100.00"))
    receiver = Account.objects.create(owner_name="Masha", balance=Decimal("50.00"))
    return sender, receiver


@pytest.mark.django_db
def test_successful_transaction(accounts):
    sender, receiver = accounts
    transaction = TransactionService.create_transaction(
        from_account=sender, to_account=receiver, amount=Decimal("30.00")
    )

    sender.refresh_from_db()
    receiver.refresh_from_db()

    assert transaction.amount == Decimal("30.00")
    assert sender.balance == Decimal("70.00")
    assert receiver.balance == Decimal("80.00")


@pytest.mark.django_db
def test_transfer_to_self_raises_error(accounts):
    sender, _ = accounts
    with pytest.raises(ValidationError, match="Cannot transfer to the same account"):
        TransactionService.create_transaction(
            from_account=sender, to_account=sender, amount=Decimal("10.00")
        )


@pytest.mark.django_db
def test_negative_amount_raises_error(accounts):
    sender, receiver = accounts
    with pytest.raises(ValidationError, match="Amount must be positive"):
        TransactionService.create_transaction(
            from_account=sender,
            to_account=receiver,
            amount=Decimal("-5.00"),
        )


@pytest.mark.django_db
def test_zero_amount_raises_error(accounts):
    sender, receiver = accounts
    with pytest.raises(ValidationError, match="Amount must be positive"):
        TransactionService.create_transaction(
            from_account=sender, to_account=receiver, amount=Decimal("0.00")
        )


@pytest.mark.django_db
def test_insufficient_funds_raises_error(accounts):
    sender, receiver = accounts
    with pytest.raises(ValidationError, match="Insufficient funds"):
        TransactionService.create_transaction(
            from_account=sender,
            to_account=receiver,
            amount=Decimal("150.00"),
        )


@pytest.mark.django_db
def test_rollback_on_failure(accounts):
    sender, receiver = accounts
    initial_sender_balance = sender.balance
    initial_receiver_balance = receiver.balance

    try:
        TransactionService.create_transaction(
            from_account=sender,
            to_account=receiver,
            amount=Decimal("150.00"),
        )
    except ValidationError:
        pass

    sender.refresh_from_db()
    receiver.refresh_from_db()

    assert sender.balance == initial_sender_balance
    assert receiver.balance == initial_receiver_balance
