from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from accounts.models import User

from rest_framework import serializers

User._meta.get_field('email')._unique = True
User._meta.get_field('username')._unique = True


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'city', 'state', 'zip')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'name', 'city', 'state', 'zip')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
            name=validated_data['name'],
            city=validated_data['city'],
            state=validated_data['state'],
            zip=validated_data['zip']
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")