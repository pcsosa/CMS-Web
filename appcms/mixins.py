from django.shortcuts import redirect
from keycloak import KeycloakOpenID

class KeycloakRoleRequiredMixin:
    """
    Esta clase controla las vistas, es decir, no permite a los usuarios sin permisos acceder a las vistas
    """
    required_roles = []

    def dispatch(self, request, *args, **kwargs):
        keycloak_openid = KeycloakOpenID(
            server_url="http://keycloak-server/auth/",
            client_id="your-client-id",
            realm_name="your-realm",
            client_secret_key="your-client-secret"
        )
        user_roles = keycloak_openid.get_user_roles(token=request.user.token)

        if any(role in user_roles for role in self.required_roles):
            return super().dispatch(request, *args, **kwargs)
        return redirect('no_permission_view')
