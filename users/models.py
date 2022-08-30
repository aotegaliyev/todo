from django.contrib.auth.models import User as DjangoUser
from django.db import models


class Profile(models.Model):
    ROLES = (
        ('admin', 'admin'),  # Админ
        ('employee', 'employee'),  # Работник
        ('client', 'client'),  # Клиент
    )

    user = models.OneToOneField(DjangoUser, null=True, blank=True, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=50, choices=ROLES, null=False)
    phone = models.CharField(max_length=20, null=True, blank=True, unique=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'user_profiles'

    def __str__(self):
        return '{}, role: {}'.format(self.user.first_name, self.role)

    @staticmethod
    def get_user_roles(roles=ROLES):
        return [role[0] for role in roles]
