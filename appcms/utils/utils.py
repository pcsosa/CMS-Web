def comprobarToken(request, token, kc):
    if not kc.isActive(token['access_token']):
      print("RENOVANDO TOKEN...")
      newToken = kc.renovarToken(token)
      request.session['token'] = newToken
      return newToken
    else:
      return token