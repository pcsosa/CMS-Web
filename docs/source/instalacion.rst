Instalación y Configuración del Proyecto Django
===============================================

Este documento detalla el proceso para instalar y configurar un proyecto Django utilizando un entorno virtual (`venv`), PostgreSQL como base de datos, y el archivo `.env` para la configuración del entorno.

Requisitos Previos
------------------

- Python 3.x
- PostgreSQL
- pip

Creación del Entorno Virtual
----------------------------

1. Navega al directorio del proyecto:
   
   .. code-block:: bash

      cd /ruta/a/tu/proyecto

2. Crea un entorno virtual:
   
   .. code-block:: bash

      python -m venv venv

3. Activa el entorno virtual:

   - En Windows:
     
     .. code-block:: bash

        venv\Scripts\activate

   - En macOS/Linux:
     
     .. code-block:: bash

        source venv/bin/activate

Instalación de Dependencias
---------------------------

1. Instala las dependencias del proyecto usando `pip`:

   .. code-block:: bash

      pip install -r requirements.txt

Configuración de Variables de Entorno
--------------------------------------

1. Crea un archivo `.env` en el directorio raíz del proyecto. Ejemplo de contenido:

   .. code-block:: ini

      DEBUG=True
      SECRET_KEY=tu_clave_secreta
      DATABASE_URL=postgres://usuario:contraseña@localhost:puerto/nombre_basedatos

   - Reemplaza `tu_clave_secreta` con una clave secreta segura.
   - Ajusta `DATABASE_URL` con los detalles de tu base de datos PostgreSQL.

Configuración de la Base de Datos
----------------------------------

1. Asegúrate de que PostgreSQL esté en funcionamiento y crea una base de datos para tu proyecto Django.

2. Aplica las migraciones iniciales de la base de datos:

   .. code-block:: bash

      python manage.py makemigrations
      python manage.py migrate

   - `makemigrations` crea archivos de migración para los cambios en los modelos.
   - `migrate` aplica esas migraciones a la base de datos.

Ejecución del Servidor de Desarrollo
-------------------------------------

1. Inicia el servidor de desarrollo de Django:

   .. code-block:: bash

      python manage.py runserver

   - Accede a tu aplicación web en `http://127.0.0.1:8000/`.

Conclusión
----------

Siguiendo estos pasos, deberías tener tu proyecto Django configurado y funcionando con PostgreSQL. Para cualquier problema adicional, consulta la documentación oficial de Django o revisa los mensajes de error proporcionados.
