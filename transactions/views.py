from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Transaction
from .serializers import TransactionSerializer


# 🔥 PAGINATION CLASS
class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    pagination_class = CustomPagination

    # 🔐 ROLE-BASED PERMISSIONS
    def get_permissions(self):
        user = self.request.user

        if not user.is_authenticated:
            return [IsAuthenticated()]

        if user.role == 'admin':
            return [IsAuthenticated()]

        elif user.role == 'analyst':
            if self.action in ['list', 'retrieve']:
                return [IsAuthenticated()]
            return []

        elif user.role == 'data_entry':
            if self.action == 'create':
                return [IsAuthenticated()]
            return []

        elif user.role == 'viewer':
            if self.action in ['list', 'retrieve']:
                return [IsAuthenticated()]
            return []

        return []

    # 🔥 DATA ACCESS + SEARCH + DATE FILTER
    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return Transaction.objects.none()

        queryset = Transaction.objects.all()

        # 🔍 GLOBAL SEARCH
        search = self.request.query_params.get('search')

        if search:
            query = Q(category__icontains=search) | \
                    Q(type__icontains=search) | \
                    Q(note__icontains=search)
        
            # 🔥 TRY AMOUNT SEARCH
            try:
                amount_value = float(search)
                query = query | Q(amount=amount_value)
            except:
                pass
            
            queryset = queryset.filter(query)

        # 🔍 CATEGORY FILTER
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__icontains=category)

        # 🔍 TYPE FILTER
        type_ = self.request.query_params.get('type')
        if type_:
            queryset = queryset.filter(type=type_)

        # 📅 DATE FILTER
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date:
            queryset = queryset.filter(date__gte=start_date)

        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        # 🔐 ROLE CONTROL
        if user.role == 'admin':
            return queryset

        elif user.role == 'analyst':
            return queryset

        elif user.role == 'data_entry':
            return queryset.filter(created_by=user)

        elif user.role == 'viewer':
            return queryset

        return Transaction.objects.none()

    # 🔥 AUTO-ASSIGN USER
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)