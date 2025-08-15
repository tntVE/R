from flask import Blueprint

def register_blueprint(app):
    from app.calendar_api.routes import bp
    app.register_blueprint(bp, url_prefix='/api/calendar')