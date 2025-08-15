# Usamos una imagen oficial de Python como base
FROM python:3.11-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# ---- INICIO DE CAMBIOS: Usuario no-root ----
# Creamos un usuario y grupo no-root
ARG UID=1000
ARG GID=1000
RUN groupadd -r appuser -g ${GID} && useradd -r -g appuser -u ${UID} appuser

# Copiamos el archivo de requerimientos primero para aprovechar el cache de Docker
COPY requirements.txt requirements.txt

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código de la aplicación al directorio de trabajo
COPY . .

# Cambiamos la propiedad del directorio de la aplicación al usuario no-root
RUN chown -R appuser:appuser /app

# ---- INICIO DE CAMBIOS: entrypoint.sh y permisos ----
# Copiamos y damos permisos de ejecución al script de entrada (como root)
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
# ---- FIN DE CAMBIOS: entrypoint.sh y permisos ----

# Cambiamos al usuario no-root para las siguientes instrucciones y para la ejecución
USER appuser
# ---- FIN DE CAMBIOS: Usuario no-root ----

# Definimos el script como el punto de entrada
ENTRYPOINT ["./entrypoint.sh"]

# Exponemos el puerto en el que correrá la aplicación
EXPOSE 5000

# Definimos las variables de entorno para Flask
ENV FLASK_APP=run.py

# ---- INICIO DE CAMBIOS: Gunicorn ----
# El comando para correr la aplicación cuando se inicie el contenedor
# AHORA SIN OAUTHLIB_INSECURE_TRANSPORT
CMD ["/usr/local/bin/gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "run:app"]
# ---- FIN DE CAMBIOS: Gunicorn ----
