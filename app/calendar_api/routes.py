from flask import Blueprint, jsonify, request, current_app
from flask_login import login_required, current_user
from app.services import gcalendar_service
import datetime
import pytz

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
    data = request.get_json()
    if not data:
        return jsonify({"error": "Se requiere JSON con los datos de la cita."}), 400

    summary = data.get('summary')
    description = data.get('description', '')
    start_time_str = data.get('start_time')
    end_time_str = data.get('end_time')
    attendees = data.get('attendees', [])
    calendar_id = data.get('calendar_id', 'primary')

    if not all([summary, start_time_str, end_time_str]):
        return jsonify({"error": "Faltan campos requeridos: summary, start_time, end_time."}), 400

    try:
        # Convertir strings a objetos datetime con zona horaria
        # Asumimos que los strings vienen en formato ISO 8601 y en la zona horaria de Santiago
        timezone = pytz.timezone(current_user.timezone) # Modified
        start_time = datetime.datetime.fromisoformat(start_time_str).astimezone(timezone)
        end_time = datetime.datetime.fromisoformat(end_time_str).astimezone(timezone)
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