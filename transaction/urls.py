from django.urls import path
from .views import TransactionList, TransactionDetail

urlpatterns = [
    path('', TransactionList.as_view(), name='transaction-list'),
    path('<int:pk>', TransactionDetail.as_view(), name='transaction-detail'),
]
