# appcms/templatetags/permisos.py
import ast
import os

from django.conf import settings
from django.template import Library

from ..services.keycloak_service import KeycloakService
from ..utils import utils

register = Library()


@register.simple_tag(takes_context=True)
def tienePermiso(context, resource, scopes_to_check):

    list_scopes = ast.literal_eval(scopes_to_check)

    if settings.TESTING == "True":
        return {scope: True for scope in list_scopes}

    request = context["request"]
    token = utils.obtenerToken(request)
    result = utils.tienePermiso(token, resource, list_scopes)
    return result
