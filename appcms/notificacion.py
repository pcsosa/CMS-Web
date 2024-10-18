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
    asunto = f'Edicion de categoria {categoria.nombre}'
    mensaje = f'La categoria"{categoria.nombre}" ha sido editada.'
    autores = obtenerUsersConRol('Autor')
    editores = obtenerUsersConRol('Editor')
    publicadores = obtenerUsersConRol('Publicador')
    destinatarios = [obtenerUserInfoById(usuario['id']).get("email") for usuario in autores ] + [obtenerUserInfoById(usuario['id']).get("email") for usuario in editores ] + [obtenerUserInfoById(usuario['id']).get("email") for usuario in publicadores ]

    # Enviar correo a todos los editores
    enviar_notificacion(asunto, mensaje,destinatarios)
    
def notificar_borrar_categoria(categoria):
    asunto = f'Edicion de eliminada: {categoria.nombre}'
    mensaje = f'La categoria"{categoria.nombre}" ha sido eliminada.'
    autores = obtenerUsersConRol('Autor')
    editores = obtenerUsersConRol('Editor')
    publicadores = obtenerUsersConRol('Publicador')
    destinatarios = [obtenerUserInfoById(usuario['id']).get("email") for usuario in autores ] + [obtenerUserInfoById(usuario['id']).get("email") for usuario in editores ] + [obtenerUserInfoById(usuario['id']).get("email") for usuario in publicadores ]
    # Enviar correo a todos los editores
    enviar_notificacion(asunto, mensaje,destinatarios)
    