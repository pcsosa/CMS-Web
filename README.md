
# CMS Web

Content Management System hecho en Django.


## Requisitos

- Linux, MacOS o WSL
- Python 3+
- PostgreSQL

## Instalación

Clonar el repositorio.

```bash
  git clone https://github.com/pcsosa/CMS-Web.git
```
Navegar al directorio.

```bash
  cd CMS-Web
```

Crear entorno virtual.

```bash
  python3 -m venv .venv
```

Activar entorno virtual.

```bash
  source .venv/bin/activate
```

Instalar los requerimientos.

```bash
  pip install -r requirements.txt
```

Necesitas crear el archivo `.env` en la raiz del repositorio y agregar las siguientes variables
```
DB_NAME = '<nombre base de datos>'
DB_USER = '<nombre de usuario>'
DB_PASSWORD = '<contraseña>'
DB_HOST = 'localhost'
DB_PORT = '5432'
```
Realizar las migraciones a la base de datos.

```bash
  python3 manage.py makemigrations
  python3 manage.py migrate
```

Iniciar el servidor.

```bash
  python3 manage.py runserver
```
