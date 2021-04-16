from django.urls import path

from .views import UserRegisterView, BlacklistTokenUpdateView, UserLoginView, RegisterEmailConfirm

app_name = 'users'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('email-verification/<token>/', RegisterEmailConfirm.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='logout'),
    path('logout/', BlacklistTokenUpdateView.as_view(), name='logout'),
]
