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


class ReportView(APIView):
    def get(self, request):
        # Get the report type from the query parameter
        report_type = request.query_params.get('report_type')
        if report_type == 'monthly_summary':
            report_data = self.generate_monthly_summary()
        elif report_type == 'category_summary':
            report_data = self.generate_category_expenses()
        else:
            return Response(
                {"error": "Invalid parameter. Query parameter 'report_type' should be "
                          "monthly_summary or category_summary."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(report_data, status=status.HTTP_200_OK)

    def generate_monthly_summary(self):
        # Generate the monthly summary report (similar to the previous example)
        # Calculating the sum of income and expenses for each month
        monthly_summary = []
        transactions = Transaction.objects.all()

        for year in range(2023, 2024):
            for month in range(1, 13):
                total_income = transactions.filter(type='income', date__year=year, date__month=month).aggregate(
                    total_income=models.Sum('amount'))['total_income'] or 0
                total_expense = transactions.filter(type='expense', date__year=year, date__month=month).aggregate(
                    total_expense=models.Sum('amount'))['total_expense'] or 0

                monthly_summary.append({
                    'year': year,
                    'month': month,
                    'total_income': total_income,
                    'total_expense': total_expense,
                })

        return monthly_summary

    def generate_category_expenses(self):
        # Generate report per categories
        categories = Transaction.objects.all().values_list('category', flat=True).distinct()
        category_summary = []
        for category in categories:
            total_income = Transaction.objects.filter(type='income', category=category).aggregate(total_expense=models.Sum('amount'))['total_expense'] or 0
            total_expense = Transaction.objects.filter(type='expense', category=category).aggregate(total_expense=models.Sum('amount'))['total_expense'] or 0
            category_summary.append({
                'category': category,
                'total_expense': total_expense,
                'total_income': total_income
            })
        return category_summary
