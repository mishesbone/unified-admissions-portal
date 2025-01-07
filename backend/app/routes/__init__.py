# This file initializes and registers blueprints for the routes in your app.

from flask import Blueprint

# Import the route modules
from app.routes.auth import auth_bp
from app.routes.applications import applications_bp
from app.routes.institutions import institutions_bp
from app.routes.search import search_bp
from app.routes.students import students_bp

# Initialize the Flask blueprint registry (optional)
routes = Blueprint('routes', __name__)

# Register the blueprints with the main Flask app
def init_app(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(applications_bp, url_prefix='/applications')
    app.register_blueprint(institutions_bp, url_prefix='/institutions')
    app.register_blueprint(search_bp, url_prefix='/search')
    app.register_blueprint(students_bp, url_prefix='/students')
