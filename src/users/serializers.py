from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import NewUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewUser
        fields = ('email', 'user_name', 'first_name', 'last_name', 'start_date', 'about', 'is_active')


class UserLoginSerializer(TokenObtainPairSerializer):

    # Custom return value when login
    def validate(self, attrs):
        data = super().validate(attrs)

        data.pop('refresh', None)
        data.pop('access', None)

        refresh = self.get_token(self.user)
        tokens = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        data.update({
            "user_name": self.user.user_name,
            "email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "start_date": self.user.start_date,
            "about": self.user.about,
            "tokens": tokens,
        })

        return data


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewUser
        fields = ('email', 'user_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user