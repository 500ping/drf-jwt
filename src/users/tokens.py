from rest_framework_simplejwt.tokens import Token
from datetime import timedelta

class CustomToken(Token):
    token_type = 'access'
    # lifetime = timedelta(days=3)
    lifetime = timedelta(minutes=1)