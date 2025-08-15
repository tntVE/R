from app import db
from app.utils.encrypted_type import EncryptedType # Importamos nuestro nuevo tipo

class Credencial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_doctor = db.Column(db.String(128), unique=True, nullable=False)
    
    # Usamos EncryptedType para las columnas sensibles
    token = db.Column(EncryptedType, nullable=False)
    refresh_token = db.Column(EncryptedType, nullable=False)
    token_uri = db.Column(EncryptedType, nullable=False)
    # client_id = db.Column(EncryptedType, nullable=False) # Eliminado
    # client_secret = db.Column(EncryptedType, nullable=False) # Eliminado
    scopes = db.Column(EncryptedType, nullable=False)
    
    # _temp_column ha sido eliminada

    def __repr__(self):
        return f'<Credencial {self.nombre_doctor}>'
