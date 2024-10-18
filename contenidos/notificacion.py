from django.db.models.signals import post_save
from django.dispatch import receiver
from contenidos.models_cont import Comentario,Contenido
from appcms.utils.utils import (
    obtenerUserInfoById,
    obtenerUsersConRol,
    enviar_notificacion,
)


#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
#Notificacion para contenido
@receiver(post_save, sender=Contenido)
def notificar_nuevo_contenido(sender, instance, created, **kwargs):
    if created:
        # Un nuevo comentario ha sido creado
        asunto = f'Contenido creado en'
        mensaje = f'Un nuevo contenido ha sido creado .'
        autor_id= instance.autor_id
        email = obtenerUserInfoById(autor_id).get("email")
        destinatarios = [email]
        enviar_notificacion(asunto, mensaje, destinatarios)
        
def notificar_edicion_contenido(contenido): 
    asunto = f'Edicion de contenido {contenido.titulo}'
    mensaje = f'El contenido "{contenido.titulo}" ha sido editada.'
    autor_id= contenido.autor_id
    email = obtenerUserInfoById(autor_id).get("email")
    destinatarios= [email]
    enviar_notificacion(asunto, mensaje, destinatarios)
    
def notificar_borrar_contenido(contenido):
    asunto = f'eliminacion de contenido {contenido.titulo}'
    mensaje = f'El contenido "{contenido.titulo}" ha sido eliminado.'
    autor_id= contenido.autor_id
    email = obtenerUserInfoById(autor_id).get("email")
    destinatarios= [email]
    enviar_notificacion(asunto, mensaje, destinatarios)

@receiver(post_save, sender=Comentario)
def notificar_nuevo_comentario(sender, instance, created, **kwargs):
    if created:
        # Un nuevo comentario ha sido creado
        asunto = f'Nuevo comentario en {instance.contenido.titulo}'
        mensaje = f'Un nuevo comentario ha sido agregado al contenido "{instance.contenido.titulo}".'
        contenido_id = instance.contenido.autor_id
        autor_email= obtenerUserInfoById(contenido_id).get("email")
        destinatarios = [autor_email]
        enviar_notificacion(asunto, mensaje, destinatarios)

#notificacion para cambio de estado
def enviar_notificacion_cambio_estado(estado, contenido):
    diccionario={ 'Borrador':' guardado como borrador',
                 'Revisión':'enviado para edición',
                 'A Publicar':'enviado al publicador',
                 'Publicado':'publicado',
                 'Inactivo':'inactivado'}
    
    asunto = f'Contenido en {estado}: {contenido.titulo}'
    
    mensaje = f'El contenido "{contenido.titulo}" ha sido {diccionario[estado]}.'
    
    diccionario_Rol={'Borrador':'Autor',
                    'Revisión':'Editor',
                    'A Publicar':'Publicador',
                    'Publicado':'Suscriptor',
                    'Inactivo':'Autor'}
    # Obtiene todos los usuarios del rol en el que se va a mover elcontenido
    users = obtenerUsersConRol(diccionario_Rol[estado])  # retora una lista de los usuarios con el rol del publicador
    print(users)
    correos= [obtenerUserInfoById(usuario['id']).get("email") for usuario in users ]+ [obtenerUserInfoById(contenido.autor_id).get("email")]
    destinatarios = correos

    # Enviar correo a todos los que tengan los permisos
    enviar_notificacion(asunto, mensaje,destinatarios)
