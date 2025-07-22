import pytest
from decimal import Decimal
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import Account


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def accounts():
    sender = Account.objects.create(owner_name="Artem", balance=Decimal("100.00"))
    receiver = Account.objects.create(owner_name="Masha", balance=Decimal("50.00"))
    return sender, receiver


@pytest.mark.django_db
def test_create_transaction_success(api_client, accounts):
    sender, receiver = accounts
    url = reverse("transaction-create")
    data = {
        "from_account": str(sender.id),
        "to_account": str(receiver.id),
        "amount": "30.00",
    }
    response = api_client.post(url, data, format="json")

    assert response.status_code == 201
    assert response.data["amount"] == "30.00"

    sender.refresh_from_db()
    receiver.refresh_from_db()

    assert sender.balance == Decimal("70.00")
    assert receiver.balance == Decimal("80.00")


@pytest.mark.django_db
def test_transfer_to_self_fails(api_client, accounts):
    sender, _ = accounts
    url = reverse("transaction-create")
    data = {
        "from_account": str(sender.id),
        "to_account": str(sender.id),
        "amount": "10.00",
    }
    response = api_client.post(url, data, format="json")

    assert response.status_code == 400
    assert "Cannot transfer to the same account" in response.data["error"]


@pytest.mark.django_db
def test_negative_amount_fails(api_client, accounts):
    sender, receiver = accounts
    url = reverse("transaction-create")
    data = {
        "from_account": str(sender.id),
        "to_account": str(receiver.id),
        "amount": "-10.00",
    }
    response = api_client.post(url, data, format="json")

    assert response.status_code == 400
    assert "Amount must be positive" in response.data["error"]


@pytest.mark.django_db
def test_insufficient_funds_fails(api_client, accounts):
    sender, receiver = accounts
    url = reverse("transaction-create")
    data = {
        "from_account": str(sender.id),
        "to_account": str(receiver.id),
        "amount": "150.00",
    }
    response = api_client.post(url, data, format="json")

    assert response.status_code == 400
    assert "Insufficient funds" in response.data["error"]
