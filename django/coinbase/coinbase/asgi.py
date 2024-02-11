"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""


import os
import json
from rest_framework_simplejwt.authentication import JWTAuthentication
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from coinbase.routing import websocket_urlpatterns
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model
from rest_framework.request import Request

User = get_user_model()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

jwt_authentication = JWTAuthentication()


class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode("utf-8")
        token_param = [param.split("=") for param in query_string.split("&") if param.startswith("token=")]
        token = token_param[0][1] if token_param else None
        
        if token:
            try:

                validated_token = await self.get_validated_token(token)
                user = await self.get_user(validated_token)

                scope['user'] = user
            except Exception as e:
                raise Exception(str(e))
        # Print the scope and user information

        return await self.inner(scope, receive, send)

    @database_sync_to_async
    def get_validated_token(self, token):
        return jwt_authentication.get_validated_token(token)

    @database_sync_to_async
    def get_user(self, validated_token):
        # Assuming the user ID is stored in the 'user_id' claim
        user_id = validated_token.get('user_id')
        return User.objects.get(id=user_id)


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
       
            
                URLRouter(websocket_urlpatterns)
            
        )

})
