from django.apps import AppConfig


class SubcategoriasConfig(AppConfig):
    """
    Configuración de la aplicación Subcategorias.

    :param default_auto_field: Tipo de campo por defecto para las claves primarias.
    :param name: Nombre de la aplicación dentro del proyecto Django.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subcategorias'
