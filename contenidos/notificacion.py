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
    """
    notificar_nuevo_contenido

    Envía una notificación por correo electrónico cuando se crea un nuevo contenido.

    :param sender: El modelo que envía la señal.
    :type sender: type

    :param instance: La instancia del contenido que ha sido creado.
    :type instance: Contenido

    :param created: Un booleano que indica si se ha creado un nuevo contenido.
    :type created: bool

    :param kwargs: Parámetros adicionales que pueden ser utilizados en la señal.

    :description: 
        Esta función se activa cuando se crea un nuevo contenido y envía una notificación al autor del contenido.
        El asunto del correo está formado por el texto 'Contenido creado en', y el mensaje informa al autor 
        que un nuevo contenido ha sido creado.

    :process:
        1. Verifica si el contenido ha sido creado.
        2. Obtiene el ID del autor del contenido.
        3. Extrae el correo electrónico del autor utilizando la función `obtenerUserInfoById`.
        4. Envía la notificación al autor utilizando la función `enviar_notificacion`.

    """
    if created:
        # Un nuevo comentario ha sido creado
        asunto = f'Contenido creado en'
        mensaje = f'Un nuevo contenido ha sido creado .'
        autor_id= instance.autor_id
        email = obtenerUserInfoById(autor_id).get("email")
        destinatarios = [email]
        enviar_notificacion(asunto, mensaje, destinatarios)
        
def notificar_edicion_contenido(contenido): 
    """
    notificar_edicion_contenido

    Envía una notificación por correo electrónico cuando se edita un contenido.

    :param contenido: La instancia del contenido que ha sido editada.
    :type contenido: Contenido

    :description: 
        Esta función envía una notificación al autor del contenido editado.
        El asunto del correo está formado por el texto 'Edición de contenido' seguido del título del contenido editado.
        El mensaje informa al autor que el contenido ha sido editado.

    :process:
        1. Obtiene el ID del autor del contenido.
        2. Extrae el correo electrónico del autor utilizando la función `obtenerUserInfoById`.
        3. Envía la notificación al autor utilizando la función `enviar_notificacion`.
    """
    asunto = f'Edicion de contenido {contenido.titulo}'
    mensaje = f'El contenido "{contenido.titulo}" ha sido editada.'
    autor_id= contenido.autor_id
    email = obtenerUserInfoById(autor_id).get("email")
    destinatarios= [email]
    enviar_notificacion(asunto, mensaje, destinatarios)
    
def notificar_borrar_contenido(contenido):
    """
    notificar_borrar_contenido

    Envía una notificación por correo electrónico cuando se elimina un contenido.

    :param contenido: La instancia del contenido que ha sido eliminado.
    :type contenido: Contenido

    :description: 
        Esta función envía una notificación al autor del contenido eliminado.
        El asunto del correo está formado por el texto 'Eliminación de contenido' seguido del título del contenido eliminado.
        El mensaje informa al autor que el contenido ha sido eliminado.

    :process:
        1. Obtiene el ID del autor del contenido.
        2. Extrae el correo electrónico del autor utilizando la función `obtenerUserInfoById`.
        3. Envía la notificación al autor utilizando la función `enviar_notificacion`.
    """
    asunto = f'eliminacion de contenido {contenido.titulo}'
    mensaje = f'El contenido "{contenido.titulo}" ha sido eliminado.'
    autor_id= contenido.autor_id
    email = obtenerUserInfoById(autor_id).get("email")
    destinatarios= [email]
    enviar_notificacion(asunto, mensaje, destinatarios)

@receiver(post_save, sender=Comentario)
def notificar_nuevo_comentario(sender, instance, created, **kwargs):
    """
    notificar_nuevo_comentario

    Envía una notificación por correo electrónico cuando se crea un nuevo comentario.

    :param sender: El modelo que envía la señal.
    :type sender: type

    :param instance: La instancia del comentario que ha sido creado.
    :type instance: Comentario

    :param created: Un booleano que indica si se ha creado un nuevo comentario.
    :type created: bool

    :param kwargs: Parámetros adicionales que pueden ser utilizados en la señal.

    :description: 
        Esta función se activa cuando se crea un nuevo comentario y envía una notificación al autor del contenido asociado.
        El asunto del correo está formado por el texto 'Nuevo comentario en' seguido del título del contenido relacionado.
        El mensaje informa al autor que se ha agregado un nuevo comentario al contenido.

    :process:
        1. Verifica si el comentario ha sido creado.
        2. Obtiene el ID del autor del contenido asociado al comentario.
        3. Extrae el correo electrónico del autor utilizando la función `obtenerUserInfoById`.
        4. Envía la notificación al autor utilizando la función `enviar_notificacion`.
    """
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
    """
    enviar_notificacion_cambio_estado

    Envía una notificación por correo electrónico cuando el estado de un contenido cambia.

    :param estado: El nuevo estado del contenido.
    :type estado: str

    :param contenido: La instancia del contenido cuyo estado ha cambiado.
    :type contenido: Contenido

    :description: 
        Esta función construye un asunto y un mensaje para la notificación que indica el nuevo estado del contenido.
        El mensaje informa a los destinatarios que el contenido ha cambiado de estado y proporciona el nuevo estado en un formato legible.

    :process:
        1. Define un diccionario que relaciona cada estado con su descripción correspondiente.
        2. Crea el asunto del correo utilizando el nuevo estado y el título del contenido.
        3. Genera el mensaje del correo usando la descripción del estado correspondiente.
        4. Define un diccionario que relaciona cada estado con el rol de los usuarios que deben recibir la notificación.
        5. Obtiene todos los usuarios con el rol correspondiente al nuevo estado.
        6. Extrae los correos electrónicos de los usuarios y del autor del contenido.
        7. Envía la notificación a todos los destinatarios utilizando la función `enviar_notificacion`.
    """
    diccionario={ 'Borrador':' guardado como borrador',
                 'Revisión':'agregado a la lista de contenidos listos para su edición',
                 'A Publicar':'agregado a la lista de contenidos a publicar',
                 'Publicado':'publicado',
                 'Inactivo':'inactivado :('}
    
    asunto = f'Contenido en {estado}: {contenido.titulo}'
    
    mensaje = f'El contenido "{contenido.titulo}" ha sido {diccionario[estado]}.'
    
    diccionario_Rol={'Borrador':'Autor',
                    'Revisión':'Editor',
                    'A Publicar':'Publicador',
                    'Publicado':'Suscriptor',
                    'Inactivo':'Autor'}
    # Obtiene todos los usuarios del rol en el que se va a mover elcontenido
    
    #segun el estado se envian las notificaciones
    # Cuando se envia de vuelta a borrador, se le notifica solo al autor - SOLO
    # Cuando se envia a edicion, se le notifica solo al editor designado y al autor
    # Cuando se envia a "a publicar", se le notifica solo al publicador y al autor
    # cuando se envia a publicado, se le notifica a los suscriptores y al autor
    # Cuando se envia a inactivo, se le notifica solo al autor - SOLO
    if estado == 'Borrador':
        correos = [obtenerUserInfoById(contenido.autor_id).get("email")]
    elif estado == 'Revisión':
        correos = [obtenerUserInfoById(contenido.editor_id).get("email")]+[obtenerUserInfoById(contenido.autor_id).get("email")]
    elif estado in ('A Publicar','Publicado'):
        users = obtenerUsersConRol(diccionario_Rol[estado])
        correos = [obtenerUserInfoById(usuario['id']).get("email") for usuario in users ]+ [obtenerUserInfoById(contenido.autor_id).get("email")]
    elif estado == 'Inactivo':
        correos = [obtenerUserInfoById(contenido.autor_id).get("email")]
    

    #correos= [obtenerUserInfoById(usuario['id']).get("email") for usuario in users ]+ [obtenerUserInfoById(contenido.autor_id).get("email")]
    destinatarios = correos

    # Enviar correo a todos los que tengan los permisos
    enviar_notificacion(asunto, mensaje,destinatarios)
