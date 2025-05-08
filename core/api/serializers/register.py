from django.contrib.auth import get_user_model
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "confirm_password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        if not data.get("email"):
            raise serializers.ValidationError("Email is required.")
        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        validated_data["email"] = validated_data.get("email").lower()
        user = get_user_model()(**validated_data)
        user.set_password(validated_data.get("password"))
        user.save()
        return user
