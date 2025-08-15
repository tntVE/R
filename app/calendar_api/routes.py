from flask import Blueprint, jsonify, request, current_app
from flask_login import login_required, current_user
from app.services import gcalendar_service
import datetime
import pytz
from marshmallow import ValidationError # Added
from app.schemas import AppointmentSchema # Added

bp = Blueprint('calendar_api', __name__)

@bp.route('/list_calendars')
@login_required
def list_calendars():
    service = gcalendar_service.build_gcal_service(user_id=current_user.id)
    if not service:
        return jsonify({"error": "No se encontraron credenciales para el doctor."}), 404

    calendar_list = service.calendarList().list().execute()
    return jsonify(calendar_list.get('items', []))

@bp.route('/get_free_busy')
@login_required
def get_free_busy():
    service = gcalendar_service.build_gcal_service(user_id=current_user.id)
    if not service:
        return jsonify({"error": "No se encontraron credenciales para el doctor."}), 404
    
    # Usamos nuestra nueva función para encontrar huecos para hoy
    available_slots = gcalendar_service.find_available_slots(service)
    
    return jsonify(available_slots)

@bp.route('/book_appointment', methods=['POST'])
@login_required
def book_appointment():
    schema = AppointmentSchema() # Added
    try:
        validated_data = schema.load(request.get_json()) # Added validation
    except ValidationError as err: # Added
        return jsonify({"errors": err.messages}), 400 # Added

    summary = validated_data['summary'] # Modified
    description = validated_data.get('description', '') # Modified
    start_time_str = validated_data['start_time'] # Modified
    end_time_str = validated_data['end_time'] # Modified
    attendees = validated_data.get('attendees', []) # Modified
    calendar_id = validated_data.get('calendar_id', 'primary') # Modified

    try:
        # Convertir strings a objetos datetime con zona horaria
        # Asumimos que los strings vienen en formato ISO 8601 y en la zona horaria de Santiago
        timezone = pytz.timezone(current_user.timezone) # Modified
        start_time = start_time_str.astimezone(timezone) # Modified (Marshmallow already converted to datetime)
        end_time = end_time_str.astimezone(timezone) # Modified (Marshmallow already converted to datetime)
    except ValueError:
        return jsonify({"error": "Formato de fecha/hora inválido. Use ISO 8601."}), 400

    service = gcalendar_service.build_gcal_service(user_id=current_user.id)
    if not service:
        return jsonify({"error": "No se encontraron credenciales para el doctor."}), 404

    event_link = gcalendar_service.create_calendar_event(
        service, calendar_id, summary, description, start_time, end_time, attendees
    )

    if event_link:
        return jsonify({"message": "Cita agendada con éxito.", "link": event_link}), 201
    else:
        return jsonify({"error": "No se pudo agendar la cita."}), 500
