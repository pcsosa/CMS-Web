from django.apps import AppConfig


class ContenidoConfig(AppConfig):
    """
    Configuración de 'contenidos'.

    Define la configuración de la aplicación Django.
    
    :param default_auto_field: Define el tipo de campo automático por defecto que se usará en los modelos de esta aplicación.
    :param name: El nombre de la aplicación. Debe coincidir con el nombre del directorio que contiene la aplicación.
    
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contenidos'
    
    def ready(self):
        import contenidos.notificacion