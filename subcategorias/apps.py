from django.apps import AppConfig


class SubcategoriasConfig(AppConfig):
    """
    Configuración de la aplicación 'subcategorias'.

    Esta clase configura la aplicación Django para manejar subcategorías dentro del sistema.

    :param default_auto_field: Tipo de campo utilizado para la clave primaria automática.
    :type default_auto_field: str

    :param name: Nombre de la aplicación dentro del proyecto Django.
    :type name: str
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subcategorias'
