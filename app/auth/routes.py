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
@login_required
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

@login_required
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

    credencial_existente = Credencial.query.filter_by(user_id=current_user.id).first() # Modified
    if credencial_existente:
        # Los datos se pasan en texto plano, EncryptedType los cifrará
        credencial_existente.token = credentials.token
        credencial_existente.refresh_token = credentials.refresh_token
        credencial_existente.scopes = ','.join(credentials.scopes)
    else:
        # Los datos se pasan en texto plano, EncryptedType los cifrará
        nueva_credencial = Credencial(
            user_id=current_user.id, # Modified
            token=credentials.token,
            refresh_token=credentials.refresh_token,
            token_uri=credentials.token_uri,
            scopes=','.join(credentials.scopes)
        )
        db.session.add(nueva_credencial)
    
    db.session.commit()

    return "<h1>¡AUTORIZACIÓN FINAL COMPLETADA CON ÉXITO!</h1><p>La base de datos ahora tiene los tokens de acceso.</p>"



# New: Registration Route
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index')) # Assuming a main index route later
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'doctor') # Default role
        timezone = request.form.get('timezone', 'UTC') # Default timezone

        user = User.query.filter_by(email=email).first()
        if user is None:
            user = User(email=email, role=role, timezone=timezone)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('¡Registro exitoso! Ahora puedes iniciar sesión.')
            return redirect(url_for('auth.login'))
        flash('Ese email ya está registrado.')
    return '''
        <h1>Registro</h1>
        <form method="post">
            <p><input type="email" name="email" placeholder="Email" required></p>
            <p><input type="password" name="password" placeholder="Contraseña" required></p>
            <p><input type="text" name="role" value="doctor" hidden></p>
            <p><input type="text" name="timezone" value="UTC" hidden></p>
            <p><input type="submit" value="Registrarse"></p>
        </form>
        <p>¿Ya tienes cuenta? <a href="/auth/login">Inicia sesión aquí</a></p>
    '''

# New: Login Route
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index')) # Assuming a main index route later
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user is None or not user.check_password(password):
            flash('Email o contraseña inválidos.')
            return redirect(url_for('auth.login'))
        login_user(user)
        flash('¡Inicio de sesión exitoso!')
        return redirect(url_for('main.index')) # Assuming a main index route later
    return '''
        <h1>Iniciar Sesión</h1>
        <form method="post">
            <p><input type="email" name="email" placeholder="Email" required></p>
            <p><input type="password" name="password" placeholder="Contraseña" required></p>
            <p><input type="submit" value="Iniciar Sesión"></p>
        </form>
        <p>¿No tienes cuenta? <a href="/auth/register">Regístrate aquí</a></p>
    '''

# New: Logout Route
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.')
    return redirect(url_for('auth.login'))