import os
import tempfile
from datetime import datetime, time, timedelta
from io import BytesIO

import matplotlib.pyplot as plt
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.db.models import Q  # Para realizar búsquedas
from django.db.models import Avg, Count, DurationField, ExpressionWrapper, F, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.utils.timezone import make_aware
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from appcms.models import Categoria
from appcms.utils.utils import (
    obtenerToken,
    obtenerUserId,
    obtenerUserInfoById,
    obtenerUsersConRol,
    tienePermiso,
)
from contenidos.models_cont import (
    Categoria,
    Comentario,
    ComentarioRoles,
    Contenido,
    Visualizacion,
)
from contenidos.notificacion import *
from subcategorias.models import Subcategoria


def crear_contenido(request):
    """comneta
    Crea un nuevo contenido en el sistema a partir de los datos enviados a través del formulario.

    :param request: Objeto HttpRequest que contiene los datos de la solicitud.
    :return: Si la solicitud es POST y los datos son válidos, redirige a 'lista_contenidos'.
             Si hay errores, renderiza el formulario con mensajes de error.
    :rtype: HttpResponse
    """
    editores = obtenerUsersConRol(
        "Editor"
    )  # Obtener todos los usuarios con el rol de Editor
    categorias = (
        Categoria.objects.all()
    )  # Obtener todas las categorías para mostrarlas en el formulario
    subcategorias = Subcategoria.objects.all()  # Obtener todas las subcategorías
    sub_json = serialize("json", subcategorias)

    if request.method == "POST":
        # Obtener datos del formulario
        title = request.POST.get("title")
        content = request.POST.get("content")
        if content:
            content = content.replace("<p>", "").replace("</p>", "")
        else:
            content = ""  # O puedes decidir usar un valor predeterminado
        image = request.FILES.get("image")
        categoria = request.POST.get("categoria")
        subcategoria = request.POST.get("subcategoria")
        editor_id = request.POST.get("editor")

        # Obtener el usuario actual como el autor
        token = obtenerToken(request)
        autor_id = obtenerUserId(token)

        # Obtener el publicador
        publicador = autor_id  # Temporalmente asigna el autor como publicador

        # Imprimir todos los datos para comprobar que son correctos
        print("--------------Datos del formulario-------------")
        print(f"Título: {title}")
        print(f"Contenido: {content}")
        print(f"Imagen: {image}")
        print(f"Categoría: {categoria}")
        print(f"Subcategoría: {subcategoria}")
        print(f"Editor: {editor_id}")
        print(f"Autor: {autor_id}")
        print(f"Publicador: {publicador}")

        # Obtener la instancia del modelo Categoria con el id proporcionado
        categoria_obj = Categoria.objects.get(id_categoria=categoria)

        # Obtener la instancia del modelo Subcategoria con el id proporcionado, si existe
        subcategoria_obj = (
            Subcategoria.objects.get(id_subcategoria=subcategoria)
            if subcategoria
            else None
        )

        # Crear y guardar el nuevo contenido
        nuevo_contenido = Contenido(
            titulo=title,
            texto=content,
            imagen=image,
            categoria=categoria_obj,
            subcategoria=subcategoria_obj,
            publicador_id=publicador,  # Asigna el publicador automáticamente
            estado="Borrador",  # Estado inicial automático
            editor_id=editor_id,
            autor_id=autor_id,
        )

        # Imprimir el nuevo contenido
        print("--------------Nuevo contenido-------------")
        print(f"Título: {nuevo_contenido.titulo}")
        print(f"Texto: {nuevo_contenido.texto}")
        print(f"Imagen: {nuevo_contenido.imagen}")
        print(f"Categoría: {nuevo_contenido.categoria}")
        print(f"Subcategoría: {nuevo_contenido.subcategoria}")
        print(f"Publicador: {nuevo_contenido.publicador_id}")
        print(f"Estado: {nuevo_contenido.estado}")
        print(f"Editor: {nuevo_contenido.editor_id}")
        print(f"Autor: {nuevo_contenido.autor_id}")

        nuevo_contenido.save()

        # Redireccionar después de guardar
        return redirect("gestion_contenido")

    contexto = {"editores": editores, "categorias": categorias, "sub_json": sub_json}
    # Renderizar el formulario si la solicitud no es POST
    return render(request, "crear_contenido.html", contexto)


def lista_contenidos(request):
    """
    Muestra una lista de todos los contenidos en el sistema.

    :param request: Objeto HttpRequest que contiene los datos de la solicitud.
    :return: Respuesta renderizada con la plantilla 'lista_contenidos.html' y el contexto que incluye los contenidos.
    :rtype: HttpResponse
    """
    # Obtener todos los contenidos inicialmente
    contenidos = Contenido.objects.all()

    # Obtener todos los usuarios de los roles que pueden publicar contenido
    autores = obtenerUsersConRol("Autor")
    editores = obtenerUsersConRol("Editor")
    administradores = obtenerUsersConRol("Administrador")
    publicadores = obtenerUsersConRol("Publicador")

    # Obtener los parámetros del filtro desde la solicitud
    orden = request.GET.get("orden", "desc")  # Por defecto descendente
    categoria_id = request.GET.get("categoria")
    autor_id = request.GET.get("autor")
    busqueda = request.GET.get("busqueda", "")

    # juntar listas de objetos sin repetir
    autores = list(
        {
            usuario["id"]: usuario
            for usuario in autores + editores + administradores + publicadores
        }.values()
    )

    # Filtrar por categoría si se proporciona
    if categoria_id:
        contenidos = contenidos.filter(categoria_id=categoria_id)

    # Filtrar por autor si se proporciona
    if autor_id:

        contenidos = contenidos.filter(autor_id=autor_id)

    # Filtrar por búsqueda en el título o el contenido
    if busqueda:
        contenidos = contenidos.filter(
            Q(titulo__icontains=busqueda) | Q(texto__icontains=busqueda)
        )

    # Ordenar por fecha de creación
    if orden == "asc":
        contenidos = contenidos.order_by("fecha_modificacion")
    else:
        contenidos = contenidos.order_by("-fecha_modificacion")

    # Pasar la lista de contenidos y categorías al contexto
    categorias = Categoria.objects.all()
    paginator = Paginator(contenidos, 10)  # 10 contenidos por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    contexto = {
        "page_obj": page_obj,
        "contenidos": contenidos,
        "categorias": categorias,
        "busqueda": busqueda,
        "autores": autores,
    }

    return render(request, "lista_contenidos.html", contexto)


def gestion_contenido(request):
    """
    Muestra la página de gestión de contenidos, que incluye todos los contenidos disponibles.

    :param request: Objeto HttpRequest que contiene los datos de la solicitud.
    :return: Respuesta renderizada con la plantilla 'gestion_contenido.html' y el contexto que incluye los contenidos.
    :rtype: HttpResponse
    """
    contenidos = Contenido.objects.all()
    return render(request, "gestion_contenido.html", {"contenidos": contenidos})


def editar_contenido(request):
    """
    Muestra la página para editar un contenido específico.

    :param request: Objeto HttpRequest que contiene los datos de la solicitud.
    :return: Respuesta renderizada con la plantilla 'editar_contenido.html'.
    :rtype: HttpResponse
    """

    # Falta codigo para editar contenido
    return render(request, "editar_contenido.html")


def eliminar_contenido(request):
    """
    Muestra la página para eliminar un contenido específico.

    :param request: Objeto HttpRequest que contiene los datos de la solicitud.
    :return: Respuesta renderizada con la plantilla 'eliminar_contenido.html'.
    :rtype: HttpResponse
    """
    # Falta codigo para eliminar contenido
    return render(request, "eliminar_contenido.html")


@csrf_exempt
def upload_image(request):
    """
    Sube una imagen al servidor y retorna su URL.

    :param request: Objeto HttpRequest que contiene los datos de la solicitud.
    :return: Un JsonResponse con la URL de la imagen subida.
    :rtype: JsonResponse
    """
    if request.method == "POST":
        image = request.FILES["file"]
        # Guardar la imagen en el servidor
        image_url = "ruta/donde/guardas/la/imagen/" + image.name
        # Retornar la URL de la imagen
        return JsonResponse({"location": image_url})


@csrf_exempt
def eliminar_contenido(request, pk):
    """
    Elimina un objeto de tipo Contenido basado en su clave primaria (pk).

    :param request: El objeto de solicitud HTTP.
    :type request: HttpRequest
    :param pk: Clave primaria del contenido que se desea eliminar.
    :type pk: int
    :return: Redirige a la vista de gestión de contenidos si la eliminación es exitosa,
             o retorna una respuesta JSON con un error si el contenido no existe.
    :rtype: HttpResponse or JsonResponse

    Si el contenido con la clave primaria proporcionada no se encuentra en la
    base de datos, se retorna un JSON con un mensaje de error y un estado HTTP 404.
    """
    try:
        contenido = Contenido.objects.get(pk=pk)
        contenido.delete()
        notificar_borrar_contenido(contenido)
        return redirect("gestion_contenido")
    except Contenido.DoesNotExist:
        return JsonResponse({"error": "Contenido no encontrado"}, status=404)


def editar_contenido(request, pk):
    """
    Edita un objeto de tipo Contenido basado en su clave primaria (pk).

    :param request: El objeto de solicitud HTTP.
    :type request: HttpRequest
    :param pk: Clave primaria del contenido que se desea editar.
    :type pk: int
    :return: Redirige a la vista de gestión de contenidos después de guardar los cambios,
             o renderiza el formulario de edición con los datos actuales del contenido.
    :rtype: HttpResponse

    La función permite editar el título, texto, imagen, categoría, subcategoría,
    y editor de un contenido. Si no se proporciona una nueva imagen o texto,
    se mantendrán los valores originales.

    En caso de que se envíe una solicitud POST con los nuevos datos, estos se
    validan y el contenido se actualiza en la base de datos. El autor del
    contenido se obtiene utilizando un token a través de la función `obtenerToken`.

    **Contexto de la plantilla:**

    - ``contenido``: El contenido actual a editar.
    - ``editores``: Lista de usuarios con el rol de "Editor".
    - ``categorias``: Lista de todas las categorías disponibles.
    - ``sub_json``: Subcategorías serializadas en formato JSON.

    :raises Http404: Si no se encuentra un contenido con la clave primaria proporcionada.
    """

    contenido = get_object_or_404(
        Contenido, id=pk
    )  # Obtener el contenido por ID o lanzar un error 404
    editores = obtenerUsersConRol("Editor")  # Obtener los usuarios con el rol 'Editor'
    categorias = Categoria.objects.all()  # Obtener todas las categorías
    subcategorias = Subcategoria.objects.all()  # Obtener todas las subcategorías
    sub_json = serialize("json", subcategorias)

    if request.method == "POST":
        # Obtener datos del formulario
        title = request.POST.get("title")
        content = request.POST.get("content")
        image = request.FILES.get("image")
        categoria = request.POST.get("categoria")
        subcategoria = request.POST.get("subcategoria")
        editor_id = request.POST.get("editor")

        # Validar y limpiar el contenido
        if content:
            content = content.replace("<p>", "").replace("</p>", "")
        else:
            content = (
                contenido.texto
            )  # Mantener el contenido original si no se proporciona uno nuevo

        # Obtener el usuario actual como el autor
        token = obtenerToken(request)
        autor_id = obtenerUserId(token)

        # Obtener la categoría y subcategoría
        categoria_obj = Categoria.objects.get(id_categoria=categoria)
        subcategoria_obj = (
            Subcategoria.objects.get(id_subcategoria=subcategoria)
            if subcategoria
            else None
        )

        # Actualizar el contenido con los nuevos datos
        contenido.titulo = title
        contenido.texto = content
        contenido.imagen = (
            image if image else contenido.imagen
        )  # Mantener la imagen original si no se sube una nueva
        contenido.categoria = categoria_obj
        contenido.subcategoria = subcategoria_obj
        contenido.editor_id = editor_id
        contenido.autor_id = autor_id  # Mantener el autor actual

        # Guardar los cambios en el contenido
        contenido.save()
        notificar_edicion_contenido(contenido)
        # Redireccionar a la lista de contenidos después de guardar
        return redirect("gestion_contenido")

    contexto = {
        "contenido": contenido,
        "editores": editores,
        "categorias": categorias,
        "sub_json": sub_json,
    }

    # Renderizar el formulario de edición con los datos actuales del contenido
    return render(request, "editar_contenido.html", contexto)


def filtrar(lista, rol, id):
    """
    Filtra una lista de contenidos según el rol del usuario y su identificador.

    :param lista: Lista de objetos de contenido a filtrar.
    :type lista: list
    :param rol: Rol del usuario, que determina el criterio de filtrado. Puede ser uno de los siguientes: "Autor", "Editor", "Publicador" o "Administrador".
    :type rol: str
    :param id: Identificador del usuario que se usará para el filtrado en caso de roles específicos.
    :type id: int
    :return: Lista de objetos de contenido filtrados según el rol y el identificador del usuario.
    :rtype: list

    **Roles:**

    - *Autor*: Incluye solo contenidos cuyo `autor_id` coincida con el `id` proporcionado.
    - *Editor*: Incluye solo contenidos cuyo `editor_id` coincida con el `id` proporcionado.
    - *Publicador* y *Administrador*: Incluyen todos los contenidos de la lista sin filtrado adicional.

    """
    nuevo = []
    if rol == "Autor":
        for contenido in lista:
            if contenido.autor_id == id:
                nuevo += [contenido]
    elif rol == "Editor":
        for contenido in lista:
            if contenido.editor_id == id:
                nuevo += [contenido]
    elif rol in ("Publicador", "Administrador"):
        for contenido in lista:
            nuevo += [contenido]
    return nuevo


def filtrar(lista, rol, id):
    """
    Filtra una lista de contenidos según el rol del usuario y su identificador.

    :param lista: Lista de objetos de contenido a filtrar.
    :type lista: list
    :param rol: Rol del usuario, que determina el criterio de filtrado. Puede ser uno de los siguientes: "Autor", "Editor", "Publicador" o "Administrador".
    :type rol: str
    :param id: Identificador del usuario que se usará para el filtrado en caso de roles específicos.
    :type id: int
    :return: Lista de objetos de contenido filtrados según el rol y el identificador del usuario.
    :rtype: list

    **Roles:**

    - *Autor*: Incluye solo contenidos cuyo `autor_id` coincida con el `id` proporcionado.
    - *Editor*: Incluye solo contenidos cuyo `editor_id` coincida con el `id` proporcionado.
    - *Publicador* y *Administrador*: Incluyen todos los contenidos de la lista sin filtrado adicional.

    """
    nuevo = []
    if rol == "Autor":
        for contenido in lista:
            if contenido.autor_id == id:
                nuevo += [contenido]
    elif rol == "Editor":
        for contenido in lista:
            if contenido.editor_id == id:
                nuevo += [contenido]
    elif rol in ("Publicador", "Administrador"):
        for contenido in lista:
            nuevo += [contenido]
    return nuevo


def tablero_kanban(request):
    """
    Renderiza el tablero kanban mostrando los contenidos filtrados por estado.

    :param request: El objeto de solicitud HTTP.
    :type request: HttpRequest
    :return: Renderiza la plantilla "tablero_kanban.html" con el contexto de los
             contenidos filtrados por estado.
    :rtype: HttpResponse

    Los estados de los contenidos que se filtran y muestran en el tablero son:

    - "Borrador"
    - "Revisión"
    - "A Publicar"
    - "Publicado"
    - "Inactivo"

    En el contexto de la plantilla se incluyen las listas de contenidos por
    cada estado, de la siguiente manera:

    - ``borrador``: Contenidos en estado "Borrador".
    - ``en_revision``: Contenidos en estado "Revisión".
    - ``a_publicar``: Contenidos en estado "A Publicar".
    - ``publicado``: Contenidos en estado "Publicado".
    - ``inactivo``: Contenidos en estado "Inactivo".
    """
    # Obtener artículos filtrados por estado
    borrador = Contenido.objects.filter(estado="Borrador")
    en_revision = Contenido.objects.filter(estado="Revisión")
    a_publicar = Contenido.objects.filter(estado="A Publicar")
    publicado = Contenido.objects.filter(estado="Publicado")
    inactivo = Contenido.objects.filter(estado="Inactivo")

    token = obtenerToken(request)
    user_id = obtenerUserId(token)

    users_autores = obtenerUsersConRol("Autor")
    users_editores = obtenerUsersConRol("Editor")
    users_publicadores = obtenerUsersConRol("Publicador")
    users_administradores = obtenerUsersConRol("Administrador")
    rol = ""
    for user in users_autores:
        if user["id"] == user_id:
            rol = "Autor"
    for user in users_editores:
        if user["id"] == user_id:
            rol = "Editor"
    for user in users_publicadores:
        if user["id"] == user_id:
            rol = "Publicador"
    for user in users_administradores:
        if user["id"] == user_id:
            rol = "Administrador"
    borrador = filtrar(borrador, rol, user_id)
    en_revision = filtrar(en_revision, rol, user_id)
    a_publicar = filtrar(a_publicar, rol, user_id)
    publicado = filtrar(publicado, rol, user_id)
    inactivo = filtrar(inactivo, rol, user_id)

    contexto = {
        "borrador": borrador,
        "en_revision": en_revision,
        "a_publicar": a_publicar,
        "publicado": publicado,
        "inactivo": inactivo,
    }

    return render(request, "tablero_kanban.html", contexto)


def visualizar_contenido(request, pk):
    """
    Despliega la informacion de un solo contenido y los comentarios para ese contenido

    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :param pk: La clave primaria del contenido a ser desplegado
    :type pk: int
    :return: HttpResponse: La respuesta renderizada con la lista de categorías.
    """
    try:
        contenido = Contenido.objects.get(pk=pk)
        # guarla el numero de visualizaciones
        contenido.visualizaciones += 1
        contenido.save()

        Visualizacion.objects.create(contenido=contenido, fecha=timezone.now())

        comentarios = Comentario.objects.filter(contenido=pk)
        comentarios_roles = ComentarioRoles.objects.filter(contenido=pk)
        # Reemplazar el ID del usuario por su nombre de usuario en contenido
        contenido.autor_id = obtenerUserInfoById(contenido.autor_id).get("username")

        # Reemplazar el ID del usuario por su nombre de usuario en comentarios
        for comentario in comentarios:
            comentario.usuario = obtenerUserInfoById(comentario.usuario).get("username")

        # Reemplazar el ID del usuario por su nombre de usuario en comentarios
        for comentario_ in comentarios_roles:
            comentario_.usuario = obtenerUserInfoById(comentario_.usuario).get(
                "username"
            )

        # Reemplazar el ID del usuario por su nombre de usuario en comentarios
        for comentario_ in comentarios_roles:
            comentario_.usuario = obtenerUserInfoById(comentario_.usuario).get(
                "username"
            )

        return render(
            request,
            "contenido.html",
            {
                "contenido": contenido,
                "comentarios": comentarios,
                "comentarios_roles": comentarios_roles,
            },
        )
    except Contenido.DoesNotExist:
        return JsonResponse({"error": "Contenido no encontrado"}, status=404)


def cambiar_estado(request, pk, estado_actual, estado_siguiente):
    """
    Cambia el estado de un objeto de tipo Contenido, siempre y cuando los
    estados actual y siguiente sean válidos y se puedan transitar entre ellos.

    :param request: El objeto de solicitud HTTP.
    :type request: HttpRequest
    :param pk: Clave primaria del contenido que se va a actualizar.
    :type pk: int
    :param estado_actual: Estado actual del contenido.
    :type estado_actual: str
    :param estado_siguiente: Estado al cual se desea cambiar.
    :type estado_siguiente: str
    :return: Redirige a la página anterior o, si no existe, al tablero kanban.
    :rtype: HttpResponse

    Los estados disponibles son:

    - "Borrador"
    - "Revisión"
    - "A Publicar"
    - "Publicado"
    - "Inactivo"

    La función valida que los estados proporcionados sean válidos y permite
    cambios entre estados consecutivos, a excepción del estado "Inactivo".
    """
    contenido = get_object_or_404(Contenido, pk=pk)
    estados_disponibles = (
        "Borrador",
        "Revisión",
        "A Publicar",
        "Publicado",
        "Inactivo",
    )

    scopes = [
        "enviar-borrador-revision",
        "enviar-revision-Apublicar",
        "enviar-Apublicar-Publicado",
    ]
    scopes += [
        "enviar-revision-borrador",
        "enviar-Apublicar-revision",
        "enviar-Publicado-Apublicar",
    ]
    token = obtenerToken(request)
    permiso = {
        ("Borrador", "Revisión"): "enviar-borrador-revision",
        ("Revisión", "A Publicar"): "enviar-revision-Apublicar",
        ("A Publicar", "Publicado"): "enviar-Apublicar-Publicado",
        ("Revisión", "Borrador"): "enviar-revision-borrador",
        ("A Publicar", "Revisión"): "enviar-Apublicar-revision",
        ("Publicado", "A Publicar"): "enviar-Publicado-Apublicar",
    }

    scopes = [
        "enviar-borrador-revision",
        "enviar-revision-Apublicar",
        "enviar-Apublicar-Publicado",
    ]
    scopes += [
        "enviar-revision-borrador",
        "enviar-Apublicar-revision",
        "enviar-Publicado-Apublicar",
    ]
    token = obtenerToken(request)
    permiso = {
        ("Borrador", "Revisión"): "enviar-borrador-revision",
        ("Revisión", "A Publicar"): "enviar-revision-Apublicar",
        ("A Publicar", "Publicado"): "enviar-Apublicar-Publicado",
        ("Revisión", "Borrador"): "enviar-revision-borrador",
        ("A Publicar", "Revisión"): "enviar-Apublicar-revision",
        ("Publicado", "A Publicar"): "enviar-Publicado-Apublicar",
    }

    # Verifica que los estados actual y siguiente existan en la lista de estados
    if estado_actual in estados_disponibles and estado_siguiente in estados_disponibles:
        actual = estados_disponibles.index(estado_actual)
        siguiente = estados_disponibles.index(estado_siguiente)

        # Si el estado siguiente no es 'Inactivo' y el estado actual no es 'Publicado'
        if estado_siguiente != "Inactivo" and estado_actual != "Inactivo":
            # Verifica que los estados estén uno al lado del otro
            if abs(actual - siguiente) == 1 or estado_actual == "Inactivo":
                if tienePermiso(token, "contenido", scopes)[
                    permiso[(estado_actual, estado_siguiente)]
                ]:
                    contenido.estado = estado_siguiente
                    contenido.save()
                    enviar_notificacion_cambio_estado(estado_siguiente, contenido)
                    # messages.success(request, "El estado ha sido cambiado exitosamente.")
                else:
                    messages.error(
                        request,
                        "No posee los permisos necesarios para cambiar a ese estado",
                    )
            else:
                messages.error(
                    request,
                    "Error. Se debe respetar el flujo de estados de los contenidos",
                )
        else:
            contenido.estado = estado_siguiente
            contenido.save()
            enviar_notificacion_cambio_estado(estado_siguiente, contenido)
            # messages.success(request, "El contenido ha sido inactivado.")
    else:
        messages.error(request, "Error. Estados proporcionados invalidos")

    # Manejar la redirección si HTTP_REFERER no está presente
    referer = request.META.get("HTTP_REFERER")

    if referer:
        return redirect(referer)
    else:
        # Si no hay referer, redirigir a una vista por defecto
        return redirect("tablero_kanban")


def guardar_comentario(request, pk):
    """
    Guarda un comentario en un objeto de tipo Contenido.

    :param request: El objeto de solicitud HTTP.
    :type request: HttpRequest
    :param pk: Clave primaria del contenido al que se le va a añadir un comentario.
    :type pk: int
    :return: Redirige a la página de visualización del contenido.
    :rtype: HttpResponse

    Si el método HTTP es POST, la función busca un comentario en los datos de
    la solicitud, lo limpia de etiquetas HTML, y lo guarda asociado al
    contenido correspondiente. En caso de no proporcionar un comentario válido,
    se gestiona un mensaje de error.
    """
    contenido_ = get_object_or_404(Contenido, pk=pk)

    if request.method == "POST":

        # Si se esta realizando prubeas unitarias, se asigna un usuario por defecto
        if settings.TESTING == "True":
            user = "autor1"
        else:
            #  Guardar el id del usuario logeado
            user = obtenerUserId(obtenerToken(request))

        comentario_ = request.POST.get("comentario")
        if comentario_:
            comentario_ = comentario_.replace("<p>", "").replace("</p>", "")
            nuevo_comentario = Comentario(
                contenido=contenido_,
                comentario=comentario_,
                usuario=user,
                active=True,
            )
            nuevo_comentario.save()
        else:
            error_message = "El comentario no puede estar vacío."

    return redirect("visualizar_contenido", pk)


def guardar_comentario_Roles(request, pk):
    """
    Guarda un comentario desde revision, en un objeto de tipo Contenido.

    :param request: El objeto de solicitud HTTP.
    :type request: HttpRequest
    :param pk: Clave primaria del contenido al que se le va a añadir un comentario.
    :type pk: int
    :return: Redirige a la página de visualización del contenido.
    :rtype: HttpResponse

    Si el método HTTP es POST, la función busca un comentario en los datos de
    la solicitud, lo limpia de etiquetas HTML, y lo guarda asociado al
    contenido correspondiente. En caso de no proporcionar un comentario válido,
    se gestiona un mensaje de error.
    """
    contenido_ = get_object_or_404(Contenido, pk=pk)

    if request.method == "POST":
        comentario_ = request.POST.get("comentario_rol")
        if comentario_:
            comentario_ = comentario_.replace("<p>", "").replace("</p>", "")
            nuevo_comentario = ComentarioRoles(
                contenido=contenido_,
                comentario=comentario_,
                usuario=obtenerUserId(
                    obtenerToken(request)
                ),  # Guardar el id del usuario logeado
                active=True,
            )
            nuevo_comentario.save()
            cambiar_estado(request, pk, "Revisión", "Borrador")
        else:
            error_message = "El comentario no puede estar vacío."

    return redirect("visualizar_contenido", pk)


def nromegusta(request, pk):
    contenido = get_object_or_404(Contenido, id=pk)

    # Incrementar el contador de "me gusta"
    contenido.megusta += 1
    contenido.save()

    return JsonResponse({"me_gusta": contenido.megusta})


def reporte(request):
    # Obtener los parámetros de filtrado de la solicitud GET
    fecha_inicio = request.GET.get("fecha_inicio")
    fecha_fin = request.GET.get("fecha_fin")
    estado = request.GET.get("estado")

    categoria_id = request.GET.get("categoria")
    subcategoria_id = request.GET.get("subcategoria")

    # Filtrar los contenidos según los parámetros
    # contenidos = Contenido.objects.order_by('-megusta')[:5]
    contenidos = Contenido.objects.all()

    if fecha_inicio:
        fecha_inicio = parse_date(fecha_inicio)
        # Ajustar la fecha de fin para incluir todo el día
        fecha_inicio = make_aware(datetime.combine(fecha_inicio, time.min))
        contenidos = contenidos.filter(fecha_creacion__gte=fecha_inicio)
    if fecha_fin:
        fecha_fin = parse_date(fecha_fin)
        # Ajustar la fecha de fin para incluir todo el día
        fecha_fin = make_aware(datetime.combine(fecha_fin, time.max))
        contenidos = contenidos.filter(fecha_creacion__lte=fecha_fin)
    if estado:
        contenidos = contenidos.filter(estado=estado)

    if categoria_id:
        contenidos = contenidos.filter(categoria_id=categoria_id)

    if subcategoria_id:
        contenidos = contenidos.filter(subcategoria_id=subcategoria_id)

    # Calcular el resumen general
    summary = {
        "total_visitas": contenidos.aggregate(total_visitas=Sum("visualizaciones"))[
            "total_visitas"
        ]
        or 0,
        "total_megusta": contenidos.aggregate(total_megusta=Sum("megusta"))[
            "total_megusta"
        ]
        or 0,
        "total_contenido": contenidos.count() or 0,
    }

    # Calcular la cantidad de artículos redactados en el periodo de tiempo
    articulos_redactados = contenidos.count()

    # Calcular el promedio de tiempo de revisión de artículos
    tiempo_revision = None
    if fecha_inicio and fecha_fin:
        tiempo_revision = (
            Contenido.objects.filter(
                estado="Revisión",
                fecha_creacion__gte=fecha_inicio,
                fecha_creacion__lte=fecha_fin,
            )
            .annotate(
                tiempo_revision=ExpressionWrapper(
                    F("fecha_modificacion") - F("fecha_creacion"),
                    output_field=DurationField(),
                )
            )
            .aggregate(promedio_tiempo_revision=Avg("tiempo_revision"))[
                "promedio_tiempo_revision"
            ]
        )

    # Obtener los top 5 contenidos con más "me gusta"
    top_contenidos = contenidos.order_by("-megusta")[:5]

    # Obtener los top 5 contenidos más leídos en el periodo de tiempo
    if fecha_inicio and fecha_fin:
        top_leidos = (
            contenidos.filter(visualizacion__fecha__range=(fecha_inicio, fecha_fin))
            .annotate(total_visitas=Count("visualizacion__id"))
            .order_by("-total_visitas")[:5]
        )
    else:
        top_leidos = []

    # Obtener todas las categorías y subcategorías para los filtros
    categorias = Categoria.objects.all()
    subcategorias = Subcategoria.objects.all()

    return render(
        request,
        "reporte.html",
        {
            "contenidos": contenidos,
            "top_contenidos": top_contenidos,
            "top_leidos": top_leidos,
            "summary": summary,
            "articulos_redactados": articulos_redactados,
            "tiempo_revision": tiempo_revision,
            "categorias": categorias,
            "subcategorias": subcategorias,
        },
    )

    # return render(request, 'reporte.html', {
    #'contenidos': contenidos.order_by('-megusta')[:5],
    #'summary': summary,
    # })
    # return render(request, 'reporte.html', {'contenidos': contenidos, 'summary': summary})


# Para impresion en pdf


def generar_reporte_pdf(request):
    # Calcular el resumen
    summary = {
        "total_visitas": Contenido.objects.aggregate(
            total_visitas=Sum("visualizaciones")
        )["total_visitas"],
        "total_megusta": Contenido.objects.aggregate(total_megusta=Sum("megusta"))[
            "total_megusta"
        ],
        "total_contenido": Contenido.objects.count(),
    }

    # Crear la respuesta con tipo de contenido PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="reporte_contenido.pdf"'
    pdf = canvas.Canvas(response)

    # Escribir el contenido en el PDF
    pdf.drawString(100, 750, "Reporte de Contenidos")
    pdf.drawString(100, 730, "Resumen General")
    pdf.drawString(100, 710, f"Total de Visitas: {summary['total_visitas']}")
    pdf.drawString(100, 690, f"Total de Me Gusta: {summary['total_megusta']}")
    pdf.drawString(100, 670, f"Total de Contenidos: {summary['total_contenido']}")

    # Obtener los contenidos
    contenidos = Contenido.objects.all()  # Asegúrate de obtener todos los contenidos

    # Obtener los top 5 contenidos
    top_contenidos = contenidos.order_by("-megusta")[
        :5
    ]  # Filtrar los 5 contenidos con más "me gusta"

    # Crear el gráfico
    titulos = [contenido.titulo for contenido in top_contenidos]
    megustas = [contenido.megusta for contenido in top_contenidos]

    plt.figure(figsize=(8, 4))
    plt.bar(titulos, megustas, color="lightblue")
    plt.title("Top 5 Contenidos con Más Me Gusta")
    plt.xlabel("Contenido")
    plt.ylabel("Me Gusta")

    # Guardar el gráfico en un archivo temporal
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        plt.savefig(temp_file.name)  # Guardar como PNG en el archivo temporal
        plt.close()
        temp_file_path = temp_file.name  # Guardar la ruta del archivo temporal

    # Agregar el gráfico al PDF
    pdf.drawImage(
        temp_file_path, 100, 400, width=400, height=200
    )  # Ajusta la posición y el tamaño según sea necesario

    # Terminar el documento
    pdf.showPage()
    pdf.save()

    # Eliminar el archivo temporal
    os.remove(temp_file_path)

    return response


def contar_visualizaciones(articulo_id, inicio, fin):
    return Visualizacion.objects.filter(
        articulo_id=articulo_id, fecha__range=(inicio, fin)
    ).count()


def graficar_visualizaciones(request):
    fin = timezone.now()
    inicio = fin - timedelta(days=30)  # Valor por defecto de 30 días atrás

    if request.method == "POST":
        # Obtener las fechas del formulario
        inicio = request.POST.get("fecha_inicio")
        fin = request.POST.get("fecha_fin")

        # Convertir las fechas a objetos datetime
        inicio = timezone.datetime.strptime(inicio, "%Y-%m-%d")
        fin = timezone.datetime.strptime(fin, "%Y-%m-%d")

    # Contar visualizaciones por artículo en el rango de fechas
    contenidos = Contenido.objects.all()
    datos_visualizaciones = {
        contenido.titulo: Visualizacion.objects.filter(
            contenido=contenido, fecha__range=(inicio, fin)
        ).count()
        for contenido in contenidos
    }

    # Preparar datos para el gráfico
    titulos = list(datos_visualizaciones.keys())
    conteos = list(datos_visualizaciones.values())

    return render(
        request,
        "graficar_visualizaciones.html",
        {
            "titulos": titulos,
            "conteos": conteos,
            "fecha_inicio": inicio.date(),
            "fecha_fin": fin.date(),
        },
    )
