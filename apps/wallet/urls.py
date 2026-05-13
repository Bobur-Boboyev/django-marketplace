from django.urls import path

from .views import (
    WithdrawalRequestView,
    ApproveWithdrawalView,
    RejectWithdrawalView,
    MarkWithdrawalPaidView,
    VendorTransactionListView,
)

urlpatterns = [
    path(
        "<int:vendor_id>/transactions/",
        VendorTransactionListView.as_view(),
        name="vendor-transactions",
    ),
    path("<int:vendor_id>/withdraw/", WithdrawalRequestView.as_view()),
    path("withdrawals/<int:withdrawal_id>/approve/", ApproveWithdrawalView.as_view()),
    path("withdrawals/<int:withdrawal_id>/reject/", RejectWithdrawalView.as_view()),
    path("withdrawals/<int:withdrawal_id>/paid/", MarkWithdrawalPaidView.as_view()),
]
