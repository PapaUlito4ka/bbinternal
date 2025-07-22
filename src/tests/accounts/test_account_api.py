import pytest
from decimal import Decimal
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import Account


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def account():
    return Account.objects.create(owner_name="Artem", balance=Decimal("100.00"))


@pytest.mark.django_db
def test_create_account(api_client):
    url = reverse("account-create")
    data = {"owner_name": "Masha"}
    response = api_client.post(url, data, format="json")

    assert response.status_code == 201
    assert response.data["owner_name"] == "Masha"
    assert response.data["balance"] == "0.00"


@pytest.mark.django_db
def test_list_accounts(api_client, account):
    url = reverse("account-list")
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["owner_name"] == "Artem"


@pytest.mark.django_db
def test_retrieve_account(api_client, account):
    url = reverse("account-detail", kwargs={"id": account.id})
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["owner_name"] == "Artem"


@pytest.mark.django_db
def test_retrieve_account_with_transactions(api_client, account):
    receiver = Account.objects.create(owner_name="Masha", balance=Decimal("50.00"))

    from transactions.services import TransactionService

    TransactionService.create_transaction(
        from_account=account, to_account=receiver, amount=Decimal("20.00")
    )

    url = reverse("account-detail-with-transactions", kwargs={"id": account.id})
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["owner_name"] == "Artem"
    assert len(response.data["outgoing_transactions"]) == 1
    assert response.data["outgoing_transactions"][0]["amount"] == "20.00"
