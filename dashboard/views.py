from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from transactions.models import Transaction


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        # 💰 TOTALS
        income = Transaction.objects.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
        expense = Transaction.objects.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0

        # 📊 CATEGORY-WISE EXPENSE
        category_data = Transaction.objects.filter(type='expense') \
            .values('category') \
            .annotate(total=Sum('amount'))

        return Response({
            "total_income": income,
            "total_expense": expense,
            "net_balance": income - expense,
            "category_data": list(category_data)
        })