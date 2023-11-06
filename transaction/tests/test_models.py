# app/tests/test_models.py
from django.test import TestCase
from transaction.models import Transaction


class TransactionModelTestCase(TestCase):
    def test_transaction_creation_income(self):
        transaction = Transaction.objects.create(
            amount=100.0,
            type='income',
            category='Salary',
            date='2023-01-01'
        )
        self.assertEqual(transaction.amount, 100.0)
        self.assertEqual(transaction.type, 'income')
        self.assertEqual(transaction.category, 'Salary')

    def test_transaction_creation_expense(self):
        transaction = Transaction.objects.create(
            amount=20.0,
            type='expense',
            category='Shopping',
            date='2023-01-10'
        )
        self.assertEqual(transaction.amount, 20.0)
        self.assertEqual(transaction.type, 'expense')
        self.assertEqual(transaction.category, 'Shopping')
