from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from transactions.serializers import TransactionSerializer
from transactions.services import TransactionService
from rest_framework.exceptions import ValidationError


class TransactionCreateView(generics.CreateAPIView):
    serializer_class = TransactionSerializer

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            transaction = TransactionService.create_transaction(
                from_account=validated_data["from_account"],
                to_account=validated_data["to_account"],
                amount=validated_data["amount"],
            )
            serializer = self.get_serializer(transaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
