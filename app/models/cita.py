from app import db
import datetime

class Cita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    doctor = db.Column(db.String(128), nullable=False)
    fecha_hora = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    motivo = db.Column(db.String(256))

    def __repr__(self):
        return f'<Cita para {self.paciente.nombre} el {self.fecha_hora}>'