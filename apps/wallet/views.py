from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from apps.vendors.models import Vendor
from apps.vendors.permissions import IsVendorOwner

from .serializers import WithdrawalRequestSerializer
from .services import WalletService


class WithdrawalRequestView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsVendorOwner
    ]

    def post(self, request, vendor_id):

        serializer = WithdrawalRequestSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        vendor = Vendor.objects.get(
            id=vendor_id,
            owner=request.user
        )

        withdrawal = WalletService.create_withdrawal(
            vendor=vendor,
            amount=serializer.validated_data["amount"],
            card_number=serializer.validated_data["card_number"]
        )

        return Response(
            {
                "message": "Withdrawal request created",
                "withdrawal_id": withdrawal.id,
                "status": withdrawal.status
            },
            status=status.HTTP_201_CREATED
        )


class ApproveWithdrawalView(APIView):

    permission_classes = [IsAdminUser]

    def post(self, request, withdrawal_id):
        withdrawal = WalletService.approve_withdrawal(
            withdrawal_id
        )

        return Response({
            "message": "Withdrawal approved",
            "status": withdrawal.status
        })


class RejectWithdrawalView(APIView):

    permission_classes = [IsAdminUser]

    def post(self, request, withdrawal_id):
        withdrawal = WalletService.reject_withdrawal(
            withdrawal_id=withdrawal_id,
            reason=request.data.get("reason")
        )

        return Response({
            "message": "Withdrawal rejected",
            "status": withdrawal.status
        })
    

class MarkWithdrawalPaidView(APIView):

    permission_classes = [IsAdminUser]

    def post(self, request, withdrawal_id):
        withdrawal = WalletService.mark_as_paid(
            withdrawal_id
        )

        return Response({
            "message": "Withdrawal marked as paid",
            "status": withdrawal.status
        })