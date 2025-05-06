from django.db import models
from core.api.models.base import BaseModel


class Book(BaseModel):
    author = models.ForeignKey(
        "Author", on_delete=models.SET_NULL, null=True, blank=True, related_name="books"
    )
    genre = models.ForeignKey(
        "Genre", on_delete=models.SET_NULL, null=True, blank=True, related_name="books"
    )
    title = models.CharField(max_length=255)
    total_pages = models.IntegerField()
    year = models.IntegerField()
