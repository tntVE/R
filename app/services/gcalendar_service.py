from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from app.models.credencial import Credencial
import datetime
import pytz
from flask import current_app # Importamos current_app
from app import db # Already imported, just confirming its presence

def build_gcal_service(user_id): # Modified
    creds_data = Credencial.query.filter_by(user_id=user_id).first() # Modified
    if not creds_data:
        return None
    
    # Obtenemos client_id y client_secret de la configuración de la aplicación
    client_id = current_app.config['GOOGLE_CLIENT_ID']
    client_secret = current_app.config['GOOGLE_CLIENT_SECRET']

    credentials = Credentials(
        token=creds_data.token,
        refresh_token=creds_data.refresh_token,
        token_uri=creds_data.token_uri,
        client_id=client_id, # Usamos el client_id de la configuración
        client_secret=client_secret, # Usamos el client_secret de la configuración
        scopes=creds_data.scopes.split(',')
    )

    # Si el token de acceso ha expirado, lo refrescamos
    if credentials.expired and credentials.refresh_token:
        # Construimos la configuración del cliente para refrescar el token
        client_config = {
            "web": {
                "client_id": client_id,
                "client_secret": client_secret,
                "token_uri": credentials.token_uri,
            }
        }
        # Creamos un flujo temporal para refrescar
        flow = Flow.from_client_config(
            client_config,
            scopes=credentials.scopes,
            redirect_uri='urn:ietf:wg:oauth:2.0:oob' # Este URI no se usa para refrescar, pero es requerido
        )
        flow.oauth2session.token = {
            'access_token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': client_id,
            'client_secret': client_secret,
            'scopes': credentials.scopes
        }
        flow.oauth2session.refresh_token(credentials.token_uri)
        credentials = flow.credentials
        
        # Actualizamos las credenciales en la base de datos
        creds_data.token = credentials.token
        creds_data.refresh_token = credentials.refresh_token
        db.session.add(creds_data)
        db.session.commit()


    return build('calendar', 'v3', credentials=credentials)

def find_available_slots(service, calendar_id='primary', day=None):
    """
    Encuentra huecos de 1 hora en un calendario para un día específico usando freebusy.query.
    """
    if day is None:
        day = datetime.date.today()

    timezone = pytz.timezone('America/Santiago')
    time_min = datetime.datetime.combine(day, datetime.time(9, 0)).astimezone(timezone)
    time_max = datetime.datetime.combine(day, datetime.time(17, 0)).astimezone(timezone)

    body = {
        "timeMin": time_min.isoformat(),
        "timeMax": time_max.isoformat(),
        "items": [{"id": calendar_id}]
    }

    # Usamos freebusy.query para obtener los tiempos ocupados
    free_busy_result = service.freebusy().query(body=body).execute()
    busy_slots = free_busy_result.get('calendars', {}).get(calendar_id, {}).get('busy', [])

    available_slots = []
    current_time = time_min

    while current_time < time_max:
        slot_end_time = current_time + datetime.timedelta(hours=1)
        
        is_busy = False
        for busy_slot in busy_slots:
            busy_start = datetime.datetime.fromisoformat(busy_slot['start'])
            busy_end = datetime.datetime.fromisoformat(busy_slot['end'])
            
            # Comprobamos si el hueco actual se solapa con un tiempo ocupado
            if max(current_time, busy_start) < min(slot_end_time, busy_end):
                is_busy = True
                break
        
        if not is_busy and slot_end_time <= time_max:
            available_slots.append({
                'start': current_time.isoformat(),
                'end': slot_end_time.isoformat()
            })
        
        current_time += datetime.timedelta(minutes=30) # Avanzamos en intervalos de 30 minutos
        
    return available_slots

def create_calendar_event(service, calendar_id, summary, description, start_time, end_time, attendees=None):
    """
    Crea un evento en Google Calendar.
    start_time y end_time deben ser objetos datetime con zona horaria.
    """
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': start_time.tzinfo.tzname(start_time), # Obtener el nombre de la zona horaria
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': end_time.tzinfo.tzname(end_time),
        },
        'attendees': [{'email': email} for email in attendees] if attendees else [],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60}, # 24 horas antes
                {'method': 'popup', 'minutes': 10},     # 10 minutos antes
            ],
        },
    }

    try:
        event = service.events().insert(calendarId=calendar_id, body=event).execute()
        return event.get('htmlLink')
    except Exception as e:
        print(f"Error creating event: {e}")
        return None
