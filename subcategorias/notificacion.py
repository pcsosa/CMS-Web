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
    asunto = f'Edicion de subcategoria {subcategoria.nombre}'
    mensaje = f'La subcategoria "{subcategoria.titulo}" ha sido editada.'
    autores = obtenerUsersConRol('Autor')
    editores = obtenerUsersConRol('Editor')
    publicadores = obtenerUsersConRol('Publicador')
    destinatarios = [obtenerUserInfoById(usuario['id']).get("email") for usuario in autores ] + [obtenerUserInfoById(usuario['id']).get("email") for usuario in editores ] + [obtenerUserInfoById(usuario['id']).get("email") for usuario in publicadores ]
    enviar_notificacion(asunto, mensaje, destinatarios)
    
def notificar_borrar_subcategoria(subcategoria):
    asunto = f'Edicion de subcategoria {subcategoria.nombre}'
    mensaje = f'La subcategoria "{subcategoria.nombre}" ha sido editada.'
    autores = obtenerUsersConRol('Autor')
    editores = obtenerUsersConRol('Editor')
    publicadores = obtenerUsersConRol('Publicador')
    destinatarios = [obtenerUserInfoById(usuario['id']).get("email") for usuario in autores ] + [obtenerUserInfoById(usuario['id']).get("email") for usuario in editores ] + [obtenerUserInfoById(usuario['id']).get("email") for usuario in publicadores ]
    enviar_notificacion(asunto, mensaje, destinatarios)
