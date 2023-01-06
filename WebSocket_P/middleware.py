from rest_framework_simplejwt.tokens import AccessToken
import jwt
from channels.db import database_sync_to_async
from django.conf import settings
from Users.models import User
from urllib.parse import parse_qs


class JWTAuthentication:

    def authenticate(self, key):
        try:
            AccessToken(key)
            x=jwt.decode(key, settings.SECRET_KEY, ['HS256'])
            user_id=x['user_id']
            return user_id
        except Exception as e:
            return None

@database_sync_to_async
def get_user(key):
    jwt=JWTAuthentication()
    user_id=jwt.authenticate(key)
    try:
        return User.objects.get(id=user_id)
    except:
        return None
    

class JWTMiddleware:
    
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, recieve, send):
        p=parse_qs(scope['query_string'].decode())
        try:
            x=p['token'][0]
        except:
            return None
        scope['user']= await get_user(x)
        return await self.app(scope, recieve, send)


