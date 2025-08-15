from app import db
from app.utils.encrypted_type import EncryptedType # Importamos nuestro nuevo tipo

class Credencial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_doctor = db.Column(db.String(128), unique=True, nullable=False) # Keep for now
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Added

    # Usamos EncryptedType para las columnas sensibles
    token = db.Column(EncryptedType, nullable=False)
    refresh_token = db.Column(EncryptedType, nullable=False)
    token_uri = db.Column(EncryptedType, nullable=False)
    scopes = db.Column(EncryptedType, nullable=False)

    def __repr__(self):
        return f'<Credencial {self.nombre_doctor}>'