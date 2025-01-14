from flask import Flask
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
from .models import db  # Import db from models

def create_app():
    app = Flask(__name__)
    
    # Ensure instance folder exists
    os.makedirs('instance', exist_ok=True)
    
    # Generate and save Fernet key if it doesn't exist
    env_path = '.env'
    if not os.path.exists(env_path):
        with open(env_path, 'w') as f:
            key = Fernet.generate_key().decode()
            f.write(f'FERNET_KEY={key}\n')
            f.write('MASTER_PASSWORD=admin123\n')
    
    # Load environment variables BEFORE importing routes
    load_dotenv()
    
    # Configure SQLAlchemy with absolute path
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'instance', 'app.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize db with app
    db.init_app(app)
    
    # Import routes here after environment variables are loaded
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    # Create database if it doesn't exist
    with app.app_context():
        db.create_all()
    
    return app