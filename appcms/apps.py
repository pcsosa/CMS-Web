from django.apps import AppConfig


class AppcmsConfig(AppConfig):
    """
    Configuración de 'appcms'.

    Define la configuración de la aplicación Django.
    Attributos:
        default_auto_field (str): Define el tipo de campo automático por defecto
                                  que se usará en los modelos de esta aplicación.
        name (str): El nombre de la aplicación. Debe coincidir con el nombre
                    del directorio que contiene la aplicación.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appcms'
