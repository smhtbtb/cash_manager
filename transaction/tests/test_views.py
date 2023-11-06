from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, RequestsClient
from transaction.models import Transaction
from transaction.serializers import TransactionSerializer


class TransactionViewsTestCase(APITestCase):
    def setUp(self):
        # creating a test user
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.client.force_authenticate(user=self.user)

        self.transaction1 = Transaction.objects.create(
            amount=100.0,
            type='income',
            category='Salary',
            date='2023-01-01',
        )
        self.transaction2 = Transaction.objects.create(
            amount=50.0,
            type='expense',
            category='Shopping',
            date='2023-01-10',
        )

    def test_transaction_list(self):
        url = reverse('transaction-list')
        response = self.client.get(url)

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response length
        self.assertEqual(len(response.data), 2)

        # Verify that the response matches the expected serialized data
        expected_data = TransactionSerializer([self.transaction1, self.transaction2], many=True).data
        self.assertEqual(response.data, expected_data)

    def test_transaction_list_403(self):
        self.client.logout()
        url = reverse('transaction-list')
        response = self.client.get(url)

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_transaction_detail(self):
        url = reverse('transaction-detail', args=[self.transaction1.pk])
        response = self.client.get(url)

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that the response matches the expected serialized data
        expected_data = TransactionSerializer(self.transaction1).data
        self.assertEqual(response.data, expected_data)

    def test_create_transaction(self):
        url = reverse('transaction-list')
        data = {
            'amount': 75.0,
            'type': 'expense',
            'category': 'Dining',
            'date': '2023-01-03',
        }
        response = self.client.post(url, data)

        # Verify the response status code for a successful creation
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify that the transaction is created
        self.assertEqual(Transaction.objects.count(), 3)

    def test_update_transaction(self):
        url = reverse('transaction-detail', args=[self.transaction1.pk])
        data = {
            'amount': 150.0,
            'type': 'income',
            'category': 'Bonus',
            'date': '2023-01-04',
        }
        response = self.client.put(url, data)

        # Verify the response status code for update
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that the transaction is updated
        self.transaction1.refresh_from_db()
        self.assertEqual(self.transaction1.amount, 150.0)

    def test_delete_transaction(self):
        url = reverse('transaction-detail', args=[self.transaction2.pk])
        response = self.client.delete(url)

        # Verify the response status code for deletion
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify that the transaction is deleted
        self.assertEqual(Transaction.objects.count(), 1)


class BalanceViewTestCase(APITestCase):
    def test_balance_view(self):
        # Create some sample transactions
        Transaction.objects.create(amount=100.0, type='income', category='', date='2023-01-01')
        Transaction.objects.create(amount=50.0, type='expense', category='', date='2023-01-01')

        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.client.force_authenticate(user=self.user)

        url = reverse('get-balance')
        response = self.client.get(url)

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response data contains the cumulative balance
        self.assertIn('cumulative_balance', response.data)

        # Verify the cumulative balance is calculated correctly
        cumulative_balance = float(response.data['cumulative_balance'])
        self.assertEqual(cumulative_balance, 50.0)


class ReportViewTestCase(APITestCase):
    def setUp(self):
        # creating a test user
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.client.force_authenticate(user=self.user)

        self.transaction1 = Transaction.objects.create(
            amount=100.0,
            type='income',
            category='Salary',
            date='2023-01-01 00:00:00.000000+00:00',
        )
        self.transaction2 = Transaction.objects.create(
            amount=50.0,
            type='expense',
            category='Shopping',
            date='2023-01-10 00:00:00.000000+00:00',
        )

    def test_monthly_summary_report(self):
        url = reverse('get-report')
        data = {'report_type': 'monthly_summary'}
        response = self.client.get(url, data)

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response keys
        self.assertEqual(list(response.data[0].keys()), ["year", "month", "total_income", "total_expense"])

    def test_category_expenses_report(self):
        url = reverse('get-report')
        data = {'report_type': 'category_summary'}
        response = self.client.get(url, data)

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response data
        desired_response = [
            {'category': 'Salary', 'total_expense': 0, 'total_income': 100.0},
            {'category': 'Shopping', 'total_expense': 50.0, 'total_income': 0}
        ]
        self.assertEqual(response.data, desired_response)
