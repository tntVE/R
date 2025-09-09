from flask import render_template_string, redirect, url_for
from flask_login import current_user
from app.main import bp

@bp.route('/')
def index():
    """Main landing page"""
    if current_user.is_authenticated:
        return render_template_string('''
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Dashboard</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                .header { background-color: #2196F3; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
                .nav-menu { background-color: #f0f0f0; padding: 10px; margin-bottom: 20px; border-radius: 5px; }
                .nav-menu a { margin-right: 15px; text-decoration: none; color: #333; }
                .card { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
                .card h3 { color: #2196F3; margin-top: 0; }
                .card a { text-decoration: none; color: inherit; }
                .card:hover { background-color: #f5f5f5; }
            </style>
        </head>
        <body>
            <div class="nav-menu">
                <a href="/">Inicio</a>
                <a href="/programming">Aprender a Programar</a>
                <a href="/auth/logout">Cerrar Sesión</a>
            </div>
            
            <div class="header">
                <h1>¡Bienvenido!</h1>
                <p>Hola {{ current_user.email }}. ¿Qué te gustaría hacer hoy?</p>
            </div>
            
            <div class="card">
                <a href="{{ url_for('programming.index') }}">
                    <h3>🚀 Aprender a Programar</h3>
                    <p>Comienza tu journey en el mundo de la programación con nuestros tutoriales paso a paso.</p>
                </a>
            </div>
            
            <div class="card">
                <a href="/calendar_api/list_calendars">
                    <h3>📅 Ver Calendarios</h3>
                    <p>Gestiona tus calendarios y citas de Google Calendar.</p>
                </a>
            </div>
        </body>
        </html>
        ''')
    else:
        return render_template_string('''
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Bienvenido</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                .header { background-color: #4CAF50; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
                .nav-menu { background-color: #f0f0f0; padding: 10px; margin-bottom: 20px; border-radius: 5px; }
                .nav-menu a { margin-right: 15px; text-decoration: none; color: #333; }
                .card { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
                .card h3 { color: #4CAF50; margin-top: 0; }
                .card a { text-decoration: none; color: inherit; }
                .card:hover { background-color: #f5f5f5; }
                .btn { background-color: #2196F3; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px 5px; }
            </style>
        </head>
        <body>
            <div class="nav-menu">
                <a href="/">Inicio</a>
                <a href="/programming">Aprender a Programar</a>
                <a href="/auth/login">Iniciar Sesión</a>
                <a href="/auth/register">Registrarse</a>
            </div>
            
            <div class="header">
                <h1>¡Bienvenido a nuestra plataforma!</h1>
                <p>Aquí puedes aprender a programar y gestionar tus citas.</p>
            </div>
            
            <div class="card">
                <a href="{{ url_for('programming.index') }}">
                    <h3>🚀 Aprender a Programar</h3>
                    <p>¿Quieres aprender a programar? ¡Empieza aquí! Tenemos tutoriales desde lo más básico hasta conceptos avanzados.</p>
                </a>
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <h2>¿Listo para empezar?</h2>
                <a href="{{ url_for('auth.register') }}" class="btn">Crear Cuenta</a>
                <a href="{{ url_for('auth.login') }}" class="btn">Iniciar Sesión</a>
            </div>
        </body>
        </html>
        ''')