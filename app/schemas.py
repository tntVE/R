from marshmallow import Schema, fields, validate
from marshmallow.validate import Length, Email
import datetime
import pytz

class UserRegistrationSchema(Schema):
    email = fields.String(required=True, validate=Email())
    password = fields.String(required=True, validate=Length(min=8, error="La contraseña debe tener al menos 8 caracteres."))
    role = fields.String(validate=validate.OneOf(['doctor', 'admin', 'patient'])) # Example roles
    timezone = fields.String(validate=lambda tz: tz in pytz.all_timezones, error="Zona horaria inválida.")

class UserLoginSchema(Schema):
    email = fields.String(required=True, validate=Email())
    password = fields.String(required=True)

class AppointmentSchema(Schema):
    summary = fields.String(required=True, validate=Length(min=3, max=256))
    description = fields.String(validate=Length(max=1024))
    start_time = fields.DateTime(required=True, format='iso')
    end_time = fields.DateTime(required=True, format='iso')
    attendees = fields.List(fields.String(validate=Email()))
    calendar_id = fields.String(validate=Length(min=1)) # Basic validation for calendar ID
