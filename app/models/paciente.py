from app import db

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(12), index=True, unique=True, nullable=False)
    nombre = db.Column(db.String(128), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    citas = db.relationship('Cita', backref='paciente', lazy='dynamic')

    def __repr__(self):
        return f'<Paciente {self.nombre}>'