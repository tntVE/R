from flask import redirect, url_for, session, request, current_app, jsonify, flash # Added flash
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from app.auth import bp
from app import db
from app.models.credencial import Credencial
from app.models.user import User # Added
import os
from app.services import gcalendar_service
import datetime
import pytz
from flask_login import login_user, logout_user, current_user, login_required # Added

# <-- ¡Añadido!
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
        redirect_uri=url_for('auth.callback', _external=True))

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
        state=state,
        redirect_uri=url_for('auth.callback', _external=True))

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

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
        nueva_credencial = Credencial(
            nombre_doctor="Dr. Ejemplo",
            token=credentials.token,
            refresh_token=credentials.refresh_token,
            token_uri=credentials.token_uri,
            scopes=','.join(credentials.scopes)
        )
        db.session.add(nueva_credencial)
    
    db.session.commit()

    return "<h1>¡AUTORIZACIÓN FINAL COMPLETADA CON ÉXITO!</h1><p>La base de datos ahora tiene los tokens de acceso.</p>"

def list_calendars():
    service = gcalendar_service.build_gcal_service()
    if not service:
        return jsonify({"error": "No se encontraron credenciales para el doctor.
