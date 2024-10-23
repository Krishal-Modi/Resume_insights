from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
# Create your models here
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager

class AdminManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Admin(AbstractUser):
    email = models.EmailField(unique=True)  # Add unique=True here
    birth_date = models.DateField(null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name='admin_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='admin_user_permissions')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = AdminManager()

    def __str__(self):
        return self.email
