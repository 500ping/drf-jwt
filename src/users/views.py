from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, Token
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from .serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer
from .tokens import CustomToken

from .models import NewUser
from mailer.mail import resgister_confirm


class UserLoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer


class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        req_serializer = UserRegisterSerializer(data=request.data)
        if req_serializer.is_valid():
            user = req_serializer.save()
            if user:
                response = req_serializer.data

                response['message'] = 'Check your email to verification'

                confirm_token = CustomToken.for_user(user)
                resgister_confirm(user, confirm_token) # Send email

                return Response(response, status=status.HTTP_201_CREATED)
        return Response(req_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterEmailConfirm(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        validated_token = JWTAuthentication.get_validated_token(self, token)
        user_id = validated_token['user_id']
        user = get_object_or_404(NewUser, id=user_id)
        if user:
            user.is_active = True
            user.save()
            return Response({
                "status": 'active',
                "message": 'Login now!'
            })
        return Response(status=status.HTTP_400_BAD_REQUEST)


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

