from rest_framework import generics
from accounts.models import Account
from accounts.serializers import AccountSerializer, AccountWithTransactionsSerializer


class AccountCreateView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountListView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountDetailView(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = "id"


class AccountDetailWithTransactionsView(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountWithTransactionsSerializer
    lookup_field = "id"
