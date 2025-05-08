from rest_framework import serializers

from core.api.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class AuthorCreateSerializer(AuthorSerializer):
    class Meta(AuthorSerializer.Meta):
        fields = ["name", "pseudonym"]
