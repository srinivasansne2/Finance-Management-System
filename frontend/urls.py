from django.urls import path
from .views import login_view, dashboard_view, transactions_view, delete_transaction, add_transaction, edit_transaction, logout_view, users_view, update_user, register_view

urlpatterns = [
    path('', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('transactions/', transactions_view, name='transactions'),
    path('delete/<int:id>/', delete_transaction, name='delete_transaction'),
    path('add/', add_transaction, name='add_transaction'),
    path('edit/<int:id>/', edit_transaction, name='edit_transaction'),
    path('logout/', logout_view, name='logout'),
    path('users/', users_view, name='users'),
    path('update-user/<int:id>/', update_user, name='update_user'),
    path('register/', register_view, name='register'),
]