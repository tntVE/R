import base64
from cryptography.fernet import Fernet
from sqlalchemy.types import TypeDecorator, String
from flask import current_app

class EncryptedType(TypeDecorator):
    """
    A custom SQLAlchemy type that encrypts and decrypts string data
    using Fernet symmetric encryption.
    """
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if not current_app.config.get('ENCRYPTION_KEY'):
            raise ValueError("ENCRYPTION_KEY no configurada en la aplicación.")
        
        cipher_suite = Fernet(current_app.config['ENCRYPTION_KEY'].encode())
        encrypted_value = cipher_suite.encrypt(value.encode('utf-8'))
        return base64.urlsafe_b64encode(encrypted_value).decode('utf-8')

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if not current_app.config.get('ENCRYPTION_KEY'):
            raise ValueError("ENCRYPTION_KEY no configurada en la aplicación.")

        cipher_suite = Fernet(current_app.config['ENCRYPTION_KEY'].encode())
        decoded_value = base64.urlsafe_b64decode(value.encode('utf-8'))
        decrypted_value = cipher_suite.decrypt(decoded_value)
        return decrypted_value.decode('utf-8')
