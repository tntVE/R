from flask import render_template_string, request, redirect, url_for
from app.programming import bp

@bp.route('/')
def index():
    """Programming learning home page"""
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Aprender a Programar</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .header { background-color: #2196F3; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
            .lesson-card { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .lesson-card h3 { color: #2196F3; margin-top: 0; }
            .lesson-card a { text-decoration: none; color: inherit; }
            .lesson-card:hover { background-color: #f5f5f5; }
            .nav-menu { background-color: #f0f0f0; padding: 10px; margin-bottom: 20px; border-radius: 5px; }
            .nav-menu a { margin-right: 15px; text-decoration: none; color: #333; }
        </style>
    </head>
    <body>
        <div class="nav-menu">
            <a href="/auth/login">Iniciar Sesión</a>
            <a href="/auth/register">Registrarse</a>
            <a href="/programming">Aprender a Programar</a>
        </div>
        
        <div class="header">
            <h1>🚀 Aprender a Programar</h1>
            <p>Bienvenido a tu journey de programación. Aquí encontrarás todo lo que necesitas para empezar a programar.</p>
        </div>
        
        <div class="lesson-card">
            <a href="{{ url_for('programming.conceptos_basicos') }}">
                <h3>📚 Conceptos Básicos de Programación</h3>
                <p>Aprende qué es la programación, variables, tipos de datos y conceptos fundamentales.</p>
            </a>
        </div>
        
        <div class="lesson-card">
            <a href="{{ url_for('programming.python_introduccion') }}">
                <h3>🐍 Introducción a Python</h3>
                <p>Python es un excelente lenguaje para empezar. Aprende la sintaxis básica y cómo escribir tu primer programa.</p>
            </a>
        </div>
        
        <div class="lesson-card">
            <a href="{{ url_for('programming.estructuras_control') }}">
                <h3>🔄 Estructuras de Control</h3>
                <p>If/else, bucles for y while. Aprende a controlar el flujo de tus programas.</p>
            </a>
        </div>
        
        <div class="lesson-card">
            <a href="{{ url_for('programming.funciones') }}">
                <h3>⚙️ Funciones</h3>
                <p>Organiza tu código creando funciones reutilizables.</p>
            </a>
        </div>
        
        <div class="lesson-card">
            <a href="{{ url_for('programming.ejercicios') }}">
                <h3>💻 Ejercicios Prácticos</h3>
                <p>Pon en práctica lo que has aprendido con ejercicios interactivos.</p>
            </a>
        </div>
        
        <div class="lesson-card">
            <a href="{{ url_for('programming.recursos') }}">
                <h3>📖 Recursos Adicionales</h3>
                <p>Enlaces y recursos útiles para continuar tu aprendizaje.</p>
            </a>
        </div>
    </body>
    </html>
    ''')

@bp.route('/conceptos-basicos')
def conceptos_basicos():
    """Basic programming concepts"""
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Conceptos Básicos - Aprender a Programar</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }
            .header { background-color: #4CAF50; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
            .nav-menu { background-color: #f0f0f0; padding: 10px; margin-bottom: 20px; border-radius: 5px; }
            .nav-menu a { margin-right: 15px; text-decoration: none; color: #333; }
            .concept { background-color: #f9f9f9; padding: 15px; margin: 15px 0; border-left: 4px solid #4CAF50; }
            .code-block { background-color: #2d2d2d; color: #f8f8f2; padding: 15px; border-radius: 5px; margin: 10px 0; font-family: 'Courier New', monospace; }
            .back-btn { background-color: #2196F3; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="nav-menu">
            <a href="/programming">← Volver al Inicio</a>
            <a href="/programming/python-introduccion">Siguiente: Python →</a>
        </div>
        
        <div class="header">
            <h1>📚 Conceptos Básicos de Programación</h1>
            <p>Fundamentos esenciales que todo programador debe conocer</p>
        </div>
        
        <div class="concept">
            <h2>¿Qué es la Programación?</h2>
            <p>La programación es el proceso de crear instrucciones para que una computadora realice tareas específicas. 
            Es como escribir una receta muy detallada que la computadora puede seguir paso a paso.</p>
        </div>
        
        <div class="concept">
            <h2>Variables</h2>
            <p>Las variables son como cajas donde guardamos información que podemos usar más tarde. 
            Por ejemplo, podemos guardar tu nombre, tu edad, o cualquier otro dato.</p>
            
            <div class="code-block">
# Ejemplos de variables
nombre = "Juan"
edad = 25
es_estudiante = True
            </div>
        </div>
        
        <div class="concept">
            <h2>Tipos de Datos Básicos</h2>
            <p><strong>Texto (String):</strong> Palabras y frases como "Hola mundo"</p>
            <p><strong>Números Enteros (Integer):</strong> Números como 1, 2, 100, -5</p>
            <p><strong>Números Decimales (Float):</strong> Números como 3.14, 2.5, -0.8</p>
            <p><strong>Verdadero/Falso (Boolean):</strong> Solo puede ser True o False</p>
        </div>
        
        <div class="concept">
            <h2>¿Por qué Aprender a Programar?</h2>
            <ul>
                <li>🧠 Desarrolla el pensamiento lógico</li>
                <li>🚀 Automatiza tareas repetitivas</li>
                <li>💼 Muchas oportunidades laborales</li>
                <li>🎨 Puedes crear aplicaciones, juegos, websites</li>
                <li>🌍 Puedes trabajar desde cualquier lugar</li>
            </ul>
        </div>
        
        <a href="{{ url_for('programming.python_introduccion') }}" class="back-btn">
            Siguiente: Introducción a Python →
        </a>
    </body>
    </html>
    ''')

@bp.route('/python-introduccion')
def python_introduccion():
    """Python introduction"""
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Introducción a Python - Aprender a Programar</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }
            .header { background-color: #FF9800; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
            .nav-menu { background-color: #f0f0f0; padding: 10px; margin-bottom: 20px; border-radius: 5px; }
            .nav-menu a { margin-right: 15px; text-decoration: none; color: #333; }
            .lesson { background-color: #f9f9f9; padding: 15px; margin: 15px 0; border-left: 4px solid #FF9800; }
            .code-block { background-color: #2d2d2d; color: #f8f8f2; padding: 15px; border-radius: 5px; margin: 10px 0; font-family: 'Courier New', monospace; }
            .output { background-color: #e8f5e8; padding: 10px; border-radius: 5px; margin: 10px 0; border-left: 3px solid #4CAF50; }
            .back-btn { background-color: #2196F3; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="nav-menu">
            <a href="/programming">← Inicio</a>
            <a href="/programming/conceptos-basicos">← Anterior</a>
            <a href="/programming/estructuras-control">Siguiente →</a>
        </div>
        
        <div class="header">
            <h1>🐍 Introducción a Python</h1>
            <p>Tu primer paso en el mundo de Python</p>
        </div>
        
        <div class="lesson">
            <h2>¿Por qué Python?</h2>
            <p>Python es perfecto para principiantes porque:</p>
            <ul>
                <li>✨ Sintaxis simple y clara</li>
                <li>🚀 Fácil de aprender</li>
                <li>🌟 Muy popular en la industria</li>
                <li>📚 Gran comunidad y documentación</li>
                <li>🔧 Se usa para todo: web, ciencia de datos, AI, automatización</li>
            </ul>
        </div>
        
        <div class="lesson">
            <h2>Tu Primer Programa</h2>
            <p>El tradicional "Hola Mundo":</p>
            
            <div class="code-block">
print("¡Hola Mundo!")
print("Mi primer programa en Python")
            </div>
            
            <div class="output">
                <strong>Salida:</strong><br>
                ¡Hola Mundo!<br>
                Mi primer programa en Python
            </div>
        </div>
        
        <a href="{{ url_for('programming.estructuras_control') }}" class="back-btn">
            Siguiente: Estructuras de Control →
        </a>
    </body>
    </html>
    ''')

@bp.route('/estructuras-control')
def estructuras_control():
    """Control structures - simplified version"""
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Estructuras de Control - Aprender a Programar</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }
            .header { background-color: #9C27B0; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
            .nav-menu { background-color: #f0f0f0; padding: 10px; margin-bottom: 20px; border-radius: 5px; }
            .nav-menu a { margin-right: 15px; text-decoration: none; color: #333; }
            .lesson { background-color: #f9f9f9; padding: 15px; margin: 15px 0; border-left: 4px solid #9C27B0; }
            .code-block { background-color: #2d2d2d; color: #f8f8f2; padding: 15px; border-radius: 5px; margin: 10px 0; font-family: 'Courier New', monospace; }
            .back-btn { background-color: #2196F3; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="nav-menu">
            <a href="/programming">← Inicio</a>
            <a href="/programming/python-introduccion">← Anterior</a>
            <a href="/programming/funciones">Siguiente →</a>
        </div>
        
        <div class="header">
            <h1>🔄 Estructuras de Control</h1>
            <p>Controla el flujo de tu programa</p>
        </div>
        
        <div class="lesson">
            <h2>Condicionales (if/else)</h2>
            <div class="code-block">
edad = 18
if edad >= 18:
    print("Eres mayor de edad")
else:
    print("Eres menor de edad")
            </div>
        </div>
        
        <a href="{{ url_for('programming.funciones') }}" class="back-btn">
            Siguiente: Funciones →
        </a>
    </body>
    </html>
    ''')

@bp.route('/funciones')
def funciones():
    """Functions lesson - simplified"""
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Funciones - Aprender a Programar</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }
            .header { background-color: #607D8B; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
            .nav-menu { background-color: #f0f0f0; padding: 10px; margin-bottom: 20px; border-radius: 5px; }
            .nav-menu a { margin-right: 15px; text-decoration: none; color: #333; }
            .lesson { background-color: #f9f9f9; padding: 15px; margin: 15px 0; border-left: 4px solid #607D8B; }
            .code-block { background-color: #2d2d2d; color: #f8f8f2; padding: 15px; border-radius: 5px; margin: 10px 0; font-family: 'Courier New', monospace; }
            .back-btn { background-color: #2196F3; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="nav-menu">
            <a href="/programming">← Inicio</a>
            <a href="/programming/estructuras-control">← Anterior</a>
            <a href="/programming/ejercicios">Siguiente →</a>
        </div>
        
        <div class="header">
            <h1>⚙️ Funciones</h1>
            <p>Organiza y reutiliza tu código</p>
        </div>
        
        <div class="lesson">
            <h2>Tu Primera Función</h2>
            <div class="code-block">
def saludar():
    print("¡Hola!")
    print("Bienvenido al mundo de la programación")

saludar()
            </div>
        </div>
        
        <a href="{{ url_for('programming.ejercicios') }}" class="back-btn">
            Siguiente: Ejercicios Prácticos →
        </a>
    </body>
    </html>
    ''')

@bp.route('/ejercicios')
def ejercicios():
    """Practice exercises - simplified"""
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ejercicios Prácticos - Aprender a Programar</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }
            .header { background-color: #FF5722; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
            .nav-menu { background-color: #f0f0f0; padding: 10px; margin-bottom: 20px; border-radius: 5px; }
            .nav-menu a { margin-right: 15px; text-decoration: none; color: #333; }
            .exercise { background-color: #fff3e0; padding: 15px; margin: 15px 0; border-left: 4px solid #FF5722; border-radius: 5px; }
            .back-btn { background-color: #2196F3; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="nav-menu">
            <a href="/programming">← Inicio</a>
            <a href="/programming/funciones">← Anterior</a>
            <a href="/programming/recursos">Siguiente →</a>
        </div>
        
        <div class="header">
            <h1>💻 Ejercicios Prácticos</h1>
            <p>Pon en práctica lo que has aprendido</p>
        </div>
        
        <div class="exercise">
            <h3>Ejercicio 1: Saludo Personalizado</h3>
            <p>Crea un programa que le pida al usuario su nombre y muestre un saludo personalizado.</p>
        </div>
        
        <div class="exercise">
            <h3>Ejercicio 2: Calculadora Simple</h3>
            <p>Crear un programa que sume dos números ingresados por el usuario.</p>
        </div>
        
        <a href="{{ url_for('programming.recursos') }}" class="back-btn">
            Siguiente: Recursos Adicionales →
        </a>
    </body>
    </html>
    ''')

@bp.route('/recursos')
def recursos():
    """Additional resources - simplified"""
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Recursos Adicionales - Aprender a Programar</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }
            .header { background-color: #795548; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
            .nav-menu { background-color: #f0f0f0; padding: 10px; margin-bottom: 20px; border-radius: 5px; }
            .nav-menu a { margin-right: 15px; text-decoration: none; color: #333; }
            .resource-category { background-color: #f9f9f9; padding: 15px; margin: 15px 0; border-left: 4px solid #795548; border-radius: 5px; }
            .back-btn { background-color: #2196F3; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="nav-menu">
            <a href="/programming">← Inicio</a>
            <a href="/programming/ejercicios">← Anterior</a>
        </div>
        
        <div class="header">
            <h1>📖 Recursos Adicionales</h1>
            <p>Continúa tu aprendizaje con estos recursos útiles</p>
        </div>
        
        <div class="resource-category">
            <h2>🌐 Sitios Web Recomendados</h2>
            <ul>
                <li>Python.org - Tutorial oficial</li>
                <li>Codecademy - Cursos interactivos</li>
                <li>freeCodeCamp - Plataforma gratuita</li>
            </ul>
        </div>
        
        <div class="resource-category">
            <h2>💡 Consejos para Seguir Aprendiendo</h2>
            <ul>
                <li>Practica todos los días</li>
                <li>Haz proyectos personales</li>
                <li>No tengas miedo a los errores</li>
                <li>Únete a comunidades de programación</li>
            </ul>
        </div>
        
        <a href="{{ url_for('programming.index') }}" class="back-btn">
            ← Volver al Inicio
        </a>
    </body>
    </html>
    ''')