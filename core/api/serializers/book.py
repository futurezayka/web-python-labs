from rest_framework import serializers
from core.api.models.book import Book
from core.api.serializers.author import AuthorSerializer
from core.api.serializers.genre import GenreSerializer


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    genre = GenreSerializer()

    class Meta:
        model = Book
        fields = ["id", "author", "genre", "title", "total_pages", "year"]


class CreateBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["author", "genre", "title", "total_pages", "year"]
