from flask import redirect, url_for, session, request, current_app, jsonify
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from app.auth import bp
from app import db
from app.models.credencial import Credencial
import os
from app.services import gcalendar_service
import datetime # Importar datetime
import pytz # Importar pytz

# &lt;-- ¡Añadido!
def authorize():
    # Construimos la configuración del cliente directamente desde las variables de entorno
    client_config = {
        "web": {
            "client_id": current_app.config['GOOGLE_CLIENT_ID'],
            "client_secret": current_app.config['GOOGLE_CLIENT_SECRET'],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "redirect_uris": [url_for('auth.callback', _external=True)]
        }
    }

    flow = Flow.from_client_config(
        client_config,
        scopes=['https://www.googleapis.com/auth/calendar.events', 'https://www.googleapis.com/auth/calendar.readonly'],
        redirect_uri=url_for('auth.callback', _external=True))\

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    session['state'] = state
    return redirect(authorization_url)

def callback():
    state = session['state']
    
    # Construimos la configuración del cliente directamente desde las variables de entorno
    client_config = {
        "web": {
            "client_id": current_app.config['GOOGLE_CLIENT_ID'],
            "client_secret": current_app.config['GOOGLE_CLIENT_SECRET'],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "redirect_uris": [url_for('auth.callback', _external=True)]
        }
    }

    flow = Flow.from_client_config(
        client_config,
        scopes=['https://www.googleapis.com/auth/calendar.events', 'https://www.googleapis.com/auth/calendar.readonly'],
        state=state,\
        redirect_uri=url_for('auth.callback', _external=True))\

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)\

    # Obtenemos las credenciales
    credentials = flow.credentials

    credencial_existente = Credencial.query.filter_by(nombre_doctor="Dr. Ejemplo").first()
    if credencial_existente:
        # Los datos se pasan en texto plano, EncryptedType los cifrará
        credencial_existente.token = credentials.token
        credencial_existente.refresh_token = credentials.refresh_token
        credencial_existente.scopes = ','.join(credentials.scopes)
    else:
        # Los datos se pasan en texto plano, EncryptedType los cifrará
        nueva_credencial = Credencial(\
            nombre_doctor="Dr. Ejemplo",
            token=credentials.token,
            refresh_token=credentials.refresh_token,
            token_uri=credentials.token_uri,
            scopes=','.join(credentials.scopes)
        )
        db.session.add(nueva_credencial)
    
    db.session.commit()\

    return "<h1>¡AUTORIZACIÓN FINAL COMPLETADA CON ÉXITO!</h1><p>La base de datos ahora tiene los tokens de acceso.</p>"

def list_calendars():
    service = gcalendar_service.build_gcal_service()
    if not service:
        return jsonify({"error": "No se encontraron credenciales para el doctor."}), 404
    calendar_list = service.calendarList().list().execute()
    return jsonify(calendar_list.get('items', []))

# &lt;-- ¡Añadido!
def get_free_busy():
    service = gcalendar_service.build_gcal_service()
    if not service:
        return jsonify({"error": "No se encontraron credenciales para el doctor."}), 404
    
    # Usamos nuestra nueva función para encontrar huecos para hoy
    available_slots = gcalendar_service.find_available_slots(service)
    
    return jsonify(available_slots)

# &lt;-- ¡Añadido!
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
        timezone = pytz.timezone('America/Santiago')
        start_time = datetime.datetime.fromisoformat(start_time_str).astimezone(timezone)
        end_time = datetime.datetime.fromisoformat(end_time_str).astimezone(timezone)
    except ValueError:
        return jsonify({"error": "Formato de fecha/hora inválido. Use ISO 8601."}), 400

    service = gcalendar_service.build_gcal_service()
    if not service:
        return jsonify({"error": "No se encontraron credenciales para el doctor."}), 404

    event_link = gcalendar_service.create_calendar_event(
        service, calendar_id, summary, description, start_time, end_time, attendees
    )

    if event_link:
        return jsonify({"message": "Cita agendada con éxito.", "link": event_link}), 201
    else:
        return jsonify({"error": "No se pudo agendar la cita."}), 500