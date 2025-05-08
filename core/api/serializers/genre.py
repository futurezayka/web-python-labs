from rest_framework import serializers
from core.api.models.genre import Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class GenreCreateSerializer(GenreSerializer):
    class Meta(GenreSerializer.Meta):
        fields = ["name"]
