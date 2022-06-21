from rest_framework import serializers
from users.models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        updated_user = super().update(instance, validated_data)
        updated_user.set_password(validated_data["password"])
        updated_user.save()
        return updated_user


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = auth.authenticate(email=email, password=password)

        if not user.is_active:
            raise AuthenticationFailed("La cuenta no esta habilitada")
        if not user.is_verified:
            raise AuthenticationFailed("El email no fue verificado")
        return {"email": user.email, "username": user.username, "tokens": user.tokens}