from django.db import models
from core.api.models.base import BaseModel


class Genre(BaseModel):
    name = models.CharField(max_length=255, unique=True, db_index=True)
