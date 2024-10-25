from subcategorias.models import Subcategoria
from django.db.models.signals import post_save
from appcms.utils.utils import (
    obtenerUserInfoById,
    obtenerUsersConRol,
    enviar_notificacion,
)
from django.dispatch import receiver

#Notificacion para subcategorias
@receiver(post_save, sender=Subcategoria)
def notificar_nueva_subcategoria(sender, instance, created, **kwargs):
    """
    notificar_nueva_subcategoria

    Envía una notificación por correo electrónico cuando se crea una nueva subcategoría.

    :param sender: El modelo que envía la señal.
    :type sender: type

    :param instance: La instancia de la subcategoría que ha sido creada.
    :type instance: Subcategoria

    :param created: Un booleano que indica si se ha creado una nueva subcategoría.
    :type created: bool

    :param kwargs: Parámetros adicionales que pueden ser utilizados en la señal.

    :description: 
        Esta función se activa cuando se crea una nueva subcategoría y envía una notificación a los usuarios con roles específicos.
        El asunto del correo está formado por el texto 'Nueva Subcategoría en' y el mensaje informa a los destinatarios que se ha agregado una nueva subcategoría con el nombre correspondiente.

    :process:
        1. Verifica si la subcategoría ha sido creada.
        2. Obtiene los usuarios con los roles de Autor, Editor y Publicador.
        3. Extrae los correos electrónicos de esos usuarios.
        4. Envía la notificación a todos los destinatarios utilizando la función `enviar_notificacion`.
    """
    if created:
        # Un nuevo comentario ha sido creado
        asunto = f'Nueva Subcategoria en'
        mensaje = f'Una nueva subcategoria ha sido agregada "{instance.nombre}".'
        autores = obtenerUsersConRol('Autor')
        editores = obtenerUsersConRol('Editor')
        publicadores = obtenerUsersConRol('Publicador')
        destinatarios = [obtenerUserInfoById(usuario['id']).get("email") for usuario in autores ] + [obtenerUserInfoById(usuario['id']).get("email") for usuario in editores ] + [obtenerUserInfoById(usuario['id']).get("email") for usuario in publicadores ]
        enviar_notificacion(asunto, mensaje, destinatarios)
    
def notificar_editar_subcategoria(subcategoria):
    """
    notificar_editar_subcategoria

    Envía una notificación por correo electrónico cuando se edita una subcategoría.

    :param subcategoria: La instancia de la subcategoría que ha sido editada.
    :type subcategoria: Subcategoria

    :description: 
        Esta función envía una notificación a los usuarios con roles específicos cuando se edita una subcategoría.
        El asunto del correo está formado por el texto 'Edición de subcategoría' seguido del nombre de la subcategoría editada.
        El mensaje informa a los destinatarios que la subcategoría ha sido editada.

    :process:
        1. Crea el asunto del correo utilizando el nombre de la subcategoría editada.
        2. Genera el mensaje del correo indicando que la subcategoría ha sido editada.
        3. Obtiene los usuarios con los roles de Autor, Editor y Publicador.
        4. Extrae los correos electrónicos de esos usuarios.
        5. Envía la notificación a todos los destinatarios utilizando la función `enviar_notificacion`.
    """
    asunto = f'Edicion de subcategoria {subcategoria.nombre}'
    mensaje = f'La subcategoria "{subcategoria.nombre}" ha sido editada.'
    autores = obtenerUsersConRol('Autor')
    editores = obtenerUsersConRol('Editor')
    publicadores = obtenerUsersConRol('Publicador')
    destinatarios = [obtenerUserInfoById(usuario['id']).get("email") for usuario in autores ] + [obtenerUserInfoById(usuario['id']).get("email") for usuario in editores ] + [obtenerUserInfoById(usuario['id']).get("email") for usuario in publicadores ]
    enviar_notificacion(asunto, mensaje, destinatarios)
    
def notificar_borrar_subcategoria(subcategoria):
    """
    notificar_borrar_subcategoria

    Envía una notificación por correo electrónico cuando se elimina una subcategoría.

    :param subcategoria: La instancia de la subcategoría que ha sido eliminada.
    :type subcategoria: Subcategoria

    :description: 
        Esta función envía una notificación a los usuarios con roles específicos cuando se elimina una subcategoría.
        El asunto del correo está formado por el texto 'Edición de subcategoría' seguido del nombre de la subcategoría eliminada.
        El mensaje informa a los destinatarios que la subcategoría ha sido eliminada.

    :process:
        1. Crea el asunto del correo utilizando el nombre de la subcategoría eliminada.
        2. Genera el mensaje del correo indicando que la subcategoría ha sido eliminada.
        3. Obtiene los usuarios con los roles de Autor, Editor y Publicador.
        4. Extrae los correos electrónicos de esos usuarios.
        5. Envía la notificación a todos los destinatarios utilizando la función `enviar_notificacion`.
    """
    asunto = f'Edicion de subcategoria {subcategoria.nombre}'
    mensaje = f'La subcategoria "{subcategoria.nombre}" ha sido editada.'
    autores = obtenerUsersConRol('Autor')
    editores = obtenerUsersConRol('Editor')
    publicadores = obtenerUsersConRol('Publicador')
    destinatarios = [obtenerUserInfoById(usuario['id']).get("email") for usuario in autores ] + [obtenerUserInfoById(usuario['id']).get("email") for usuario in editores ] + [obtenerUserInfoById(usuario['id']).get("email") for usuario in publicadores ]
    enviar_notificacion(asunto, mensaje, destinatarios)
