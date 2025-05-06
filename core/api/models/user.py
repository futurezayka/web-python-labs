from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from core.enums.role import Role
from core.api.models.base import BaseModel


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, db_index=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)

    groups = models.ManyToManyField(
        "auth.Group", related_name="api_user_set", blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="api_user_permissions_set", blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.role == Role.ADMIN
