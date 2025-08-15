import os

class Config:
    # CRÍTICO: SECRET_KEY debe venir del entorno. La app fallará si no está.
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # CRÍTICO: DATABASE_URL debe venir del entorno.
    # Para desarrollo, se espera una URL de PostgreSQL, por ejemplo: postgresql://user:password@host:port/database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://user:password@localhost:5432/app_db' # Valor por defecto para desarrollo si no se especifica
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CRÍTICO: El nombre del archivo de credenciales de Google debe venir del entorno.
    # Para desarrollo, puedes usar GOOGLE_CLIENT_SECRET_FILE=client_secret.json
    CLIENT_SECRET_FILE = os.environ.get('GOOGLE_CLIENT_SECRET_FILE')

    # CRÍTICO: Las credenciales de Google deben venir del entorno, no del archivo JSON.
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

    # CRÍTICO: Clave de cifrado para la base de datos. DEBE ser una variable de entorno.
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')

    # Asegurarse de que los secretos críticos estén presentes
    if not SECRET_KEY:
        raise ValueError("No se ha configurado la variable de entorno SECRET_KEY.")
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("No se ha configurado la variable de entorno DATABASE_URL.")
    if not CLIENT_SECRET_FILE and (not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET):
        raise ValueError("No se han configurado las credenciales de Google (GOOGLE_CLIENT_SECRET_FILE o GOOGLE_CLIENT_ID/SECRET).")
    if not ENCRYPTION_KEY:
        raise ValueError("No se ha configurado la variable de entorno ENCRYPTION_KEY para cifrado de BD.")

    # Add other configurations here