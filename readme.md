# Prueba Tecnica Django
## Configuracion
En caso de usar docker para la ejecucion del proyecto, se deben seguir los siguientes pasos:
- Ejecutar el comando `docker-compose up -d --build` para construir la imagen y levantar los contenedores.

En caso de usar un entorno virtual, se deben seguir los siguientes pasos:
- En el archivo `.env` se debe configurar la base de datos, el usuario y la contraseña.
- Crear un entorno virtual con python 3.8 o superior, con el comando `python -m venv venv`
- Activar el entorno virtual con el comando `source venv/bin/activate` o `venv\Scripts\activate` en windows
- Instalar las dependencias con el comando `pip install -r requirements.txt`
- Ejecutar las migraciones con el comando `python manage.py migrate`
- Ejecutar el servidor con el comando `python manage.py runserver` o `gunicorn runer.wsgi -b 0.0.0.0:8000`

## Documentacion
Para acceder a la documentacion de la API, se debe ingresar a la ruta `/swagger/` de la aplicacion.


