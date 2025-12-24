# Requisitos
- Python 3.x

# Instalación (Windows)
1) Clonar el repo
2) Crear y activar entorno virtual
	- `python -m venv venv`
	- `venv\Scripts\Activate.ps1`
3) Instalar dependencias
	- `pip install -r requirements.txt`
4) Configurar base de datos
	- `python manage.py migrate`
5) (Opcional) Crear superusuario
	- `python manage.py createsuperuser`

# Variables de entorno (recomendado)
- Copia `.env.example` a `.env` y ajusta valores.
- Variables soportadas:
  - `DJANGO_DEBUG`
  - `DJANGO_SECRET_KEY`
  - `DJANGO_ALLOWED_HOSTS` (separado por comas)
  - `DJANGO_CSRF_TRUSTED_ORIGINS` (separado por comas)

# Levantar el servidor
- Local:
  - `python manage.py runserver`

- En red (para acceder desde otra PC en la misma LAN):
  1) `python manage.py runserver 0.0.0.0:8000`
  2) En tu `.env`, agrega el IP del servidor a `DJANGO_ALLOWED_HOSTS`
	  - Ejemplo: `DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,192.168.1.50`
