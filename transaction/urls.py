from django.urls import path
from .views import TransactionList, TransactionDetail, BalanceView

urlpatterns = [
    path('', TransactionList.as_view(), name='transaction-list'),
    path('<int:pk>', TransactionDetail.as_view(), name='transaction-detail'),
    path('get-balance', BalanceView.as_view(), name='get-balance'),
]
