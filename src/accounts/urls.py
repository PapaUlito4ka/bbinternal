from django.urls import path
from accounts.views import (
    AccountCreateView,
    AccountListView,
    AccountDetailView,
    AccountDetailWithTransactionsView,
)

urlpatterns = [
    path("accounts/", AccountListView.as_view(), name="account-list"),
    path("accounts/<uuid:id>/", AccountDetailView.as_view(), name="account-detail"),
    path("accounts/create/", AccountCreateView.as_view(), name="account-create"),
    path(
        "accounts/<uuid:id>/with-transactions/",
        AccountDetailWithTransactionsView.as_view(),
        name="account-detail-with-transactions",
    ),
]
