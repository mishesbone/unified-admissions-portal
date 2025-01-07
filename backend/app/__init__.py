from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
import logging
from flask_jwt_extended import JWTManager

# Initialize the JWTManager
jwt = JWTManager()
# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change to a real secret key
    jwt.init_app(app)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, supports_credentials=True)

    # Setup logging
    logging.basicConfig(level=logging.INFO)
    app.logger.info("Initializing the Unified University Admissions Portal API")

    # Import and register blueprints
    try:
        from app.routes.auth import auth_bp
        from app.routes.applications import applications_bp
        from app.routes.institutions import institutions_bp
        from app.routes.search import search_bp
        from app.routes.students import students_bp
        from app.routes.admin import admin_bp

        
        
        
        app.register_blueprint(admin_bp, url_prefix='/admin')
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(applications_bp, url_prefix='/applications')
        app.register_blueprint(institutions_bp, url_prefix='/institutions')
        app.register_blueprint(search_bp, url_prefix='/search')
        app.register_blueprint(students_bp, url_prefix='/students')

        app.logger.info("All blueprints registered successfully.")
    except Exception as e:
        app.logger.error(f"Error registering blueprints: {e}")

    # Root route for health check
    @app.route('/')
    def index():
        try:
            # Basic health check, including database connectivity
            db.session.execute('SELECT 1')
            return {"message": "API is running and database is connected!"}, 200
        except Exception as e:
            app.logger.error(f"Health check failed: {e}")
            return {"message": "API is running, but database connectivity failed.", "error": str(e)}, 500

    return app
