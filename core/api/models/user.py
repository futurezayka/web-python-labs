from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from core.api.managers.user import UserManager
from core.enums.role import Role
from core.api.models.base import BaseModel


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    email = models.EmailField(unique=True, db_index=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)

    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
