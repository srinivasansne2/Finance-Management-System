from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        user = self.request.user

        # 🔥 1. Allow registration (POST /api/users/) without login
        if self.action == 'create':
            return []

        # 🔐 2. If not logged in → block
        if not user.is_authenticated:
            return [IsAuthenticated()]

        # 👑 3. Only admin can access user management
        if user.role == 'admin':
            return [IsAuthenticated()]

        # ❌ Others (analyst, viewer, data_entry) → no access
        return []