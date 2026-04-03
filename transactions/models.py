from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Transaction(models.Model):

    TYPE_CHOICES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    # 🔥 BASIC FIELDS
    amount = models.FloatField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    category = models.CharField(max_length=100)   # 🔥 increased length

    # 🔥 DATE (USED FOR FILTERING)
    date = models.DateField()

    # 🔥 NOTE (USED IN SEARCH)
    note = models.TextField(blank=True, null=True)   # 🔥 FIXED

    # 🔥 USER (RBAC)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # 🔥 OPTIONAL (GOOD PRACTICE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - ₹{self.amount}"