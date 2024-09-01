from django.urls import re_path
from django.views.static import serve
import os
from django.conf import settings

urlpatterns = [
    # Otros patrones de URL...

    # Ruta para servir la documentación de Sphinx
    re_path(r'^documentation/(?P<path>.*)$', serve, {
        'document_root': os.path.join(settings.BASE_DIR, 'docs/_build/html'),
    }),
]
