from appcms.utils.utils import obtenerRolesUser, obtenerToken, obtenerUserInfo


def datos_basicos(request):

    token = obtenerToken(request)

    if not token:
        return {}

    user_info = obtenerUserInfo(token)
    roles = obtenerRolesUser(token)

    contexto = {"user_info": user_info, "roles": roles}

    return contexto
