from django.conf import settings
from django.http import JsonResponse
from keycloak import KeycloakOpenID
import requests, os
from dotenv import load_dotenv
load_dotenv()

class KeycloakMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.keycloak_openid = KeycloakOpenID(server_url=os.getenv('KEYCLOAK_SERVER_URL'),
                                              client_id=os.getenv('KEYCLOAK_CLIENT_ID'),
                                              realm_name=os.getenv('KEYCLOAK_REALM'),
                                              client_secret_key=os.getenv('KEYCLOAK_CLIENT_SECRET'))

    def __call__(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token:
            token = token.replace('Bearer ', '')
            try:
                self.keycloak_openid.introspect(token)
            except Exception as e:
                return JsonResponse({'error': 'Unauthorized'}, status=401)

        response = self.get_response(request)
        return response
