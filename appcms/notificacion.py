from django.db.models.signals import post_save
from django.dispatch import receiver
from appcms.models import Categoria
from appcms.utils.utils import (
    obtenerUserInfoById,
    obtenerUsersConRol,
    enviar_notificacion,
)


@receiver(post_save, sender=Categoria)
def notificar_nueva_categoria(sender, instance, created, **kwargs):
    """
    Envía una notificación por correo electrónico cuando se crea una nueva categoría.

    Este signal se activa después de que se crea una instancia de la clase `Categoria`. 
    Verifica si la instancia fue creada (es decir, no actualizada), y luego envía 
    notificaciones a los usuarios con roles de "Autor", "Editor" y "Publicador".

    :param sender: El modelo que envió el signal. En este caso, es el modelo `Categoria`.
    :type sender: Model
    :param instance: La instancia del modelo `Categoria` que ha sido creada.
    :type instance: Categoria
    :param created: Un valor booleano que indica si la instancia fue creada (True) o 
                    actualizada (False).
    :type created: bool
    :param kwargs: Argumentos adicionales que pueden ser proporcionados por el signal.
    
    **Comportamiento:**
    - Si `created` es True (la categoría fue creada), se construye un asunto y un mensaje 
      que contiene el nombre de la nueva categoría.
    - Se obtiene una lista de destinatarios compuesta por los correos electrónicos de 
      los usuarios con roles de "Autor", "Editor" y "Publicador". Estos roles son 
      obtenidos mediante la función `obtenerUsersConRol`.
    - La función `enviar_notificacion` se utiliza para enviar el correo a los destinatarios 
      recopilados."""
    if created:
        # Un nuevo comentario ha sido creado
        asunto = f'Nueva categoria en {instance.nombre}'
        mensaje = f'Una nueva categoria ha sido agregadoa: "{instance.nombre}".'
        autores = obtenerUsersConRol('Autor')
        editores = obtenerUsersConRol('Editor')
        publicadores = obtenerUsersConRol('Publicador')
        destinatarios = [obtenerUserInfoById(usuario['id']).get("email") for usuario in autores ] + [obtenerUserInfoById(usuario['id']).get("email") for usuario in editores ] + [obtenerUserInfoById(usuario['id']).get("email") for usuario in publicadores ]
        enviar_notificacion(asunto, mensaje, destinatarios)
    
def notificar_editar_categoria(categoria):
    """
    notificar_editar_categoria

    Envía notificaciones por correo electrónico a los usuarios con roles específicos 
    (Autor, Editor y Publicador) cuando se edita una categoría.

    :param categoria: La categoría que ha sido editada.
    :type categoria: Categoria

    :description: 
        Esta función construye un asunto y un mensaje para la notificación de edición de la categoría.
        Los destinatarios del correo son los usuarios que tienen alguno de los siguientes roles:
        - **Autor**
        - **Editor**
        - **Publicador**

        El asunto del correo está formado por el texto 'Edición de categoría' seguido del nombre de la categoría editada.
        El contenido del mensaje informa a los destinatarios que la categoría ha sido editada.

    :process:
        1. Obtiene los usuarios con los roles mencionados.
        2. Extrae los correos electrónicos de esos usuarios.
        3. Envía la notificación a todos los destinatarios utilizando la función `enviar_notificacion`.
    """
    
    asunto = f'Edicion de categoria {categoria.nombre}'
    mensaje = f'La categoria"{categoria.nombre}" ha sido editada.'
    autores = obtenerUsersConRol('Autor')
    editores = obtenerUsersConRol('Editor')
    publicadores = obtenerUsersConRol('Publicador')
    destinatarios = [obtenerUserInfoById(usuario['id']).get("email") for usuario in autores ] + [obtenerUserInfoById(usuario['id']).get("email") for usuario in editores ] + [obtenerUserInfoById(usuario['id']).get("email") for usuario in publicadores ]

    # Enviar correo a todos los editores
    enviar_notificacion(asunto, mensaje,destinatarios)
    
def notificar_borrar_categoria(categoria):
    """
    notificar_borrar_categoria

    Envía notificaciones por correo electrónico a los usuarios con roles específicos 
    (Autor, Editor y Publicador) cuando se elimina una categoría.

    :param categoria: La categoría que ha sido eliminada.
    :type categoria: Categoria

    :description: 
        Esta función construye un asunto y un mensaje para la notificación de eliminación de la categoría.
        Los destinatarios del correo son los usuarios que tienen alguno de los siguientes roles:
        - **Autor**
        - **Editor**
        - **Publicador**

        El asunto del correo está formado por el texto 'Edición eliminada' seguido del nombre de la categoría eliminada.
        El contenido del mensaje informa a los destinatarios que la categoría ha sido eliminada.

    :process:
        1. Obtiene los usuarios con los roles mencionados.
        2. Extrae los correos electrónicos de esos usuarios.
        3. Envía la notificación a todos los destinatarios utilizando la función `enviar_notificacion`.
    """
    asunto = f'Edicion de eliminada: {categoria.nombre}'
    mensaje = f'La categoria"{categoria.nombre}" ha sido eliminada.'
    autores = obtenerUsersConRol('Autor')
    editores = obtenerUsersConRol('Editor')
    publicadores = obtenerUsersConRol('Publicador')
    destinatarios = [obtenerUserInfoById(usuario['id']).get("email") for usuario in autores ] + [obtenerUserInfoById(usuario['id']).get("email") for usuario in editores ] + [obtenerUserInfoById(usuario['id']).get("email") for usuario in publicadores ]
    # Enviar correo a todos los editores
    enviar_notificacion(asunto, mensaje,destinatarios)
    