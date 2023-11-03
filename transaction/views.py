from django.db import models
from rest_framework import generics, filters
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['type', 'category']
    ordering_fields = ['id', 'amount', 'date']


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]


class BalanceView(APIView):
    def get(self, request):
        calculate_balance = self.calculate_balance()
        return Response(calculate_balance, status=status.HTTP_200_OK)

    def calculate_balance(self):
        # Calculate the cumulative balance based on existing transactions
        previous_transactions = Transaction.objects.all()
        cumulative_balance = previous_transactions.filter(type='income').aggregate(
            total_income=models.Sum('amount')
        )['total_income'] or 0
        cumulative_balance -= previous_transactions.filter(type='expense').aggregate(
            total_expense=models.Sum('amount')
        )['total_expense'] or 0
        return {"cumulative_balance": float(cumulative_balance)}

