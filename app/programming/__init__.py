from flask import Blueprint

bp = Blueprint('programming', __name__)

from app.programming import routes