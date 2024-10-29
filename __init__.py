from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

# Initialize the SQLAlchemy instance
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configure the database URI from environment variables
    database_url = os.getenv("DATABASE_URL")
    print(f"Database URL: {database_url}")  # Useful for debugging
    if not database_url:
        raise ValueError("DATABASE_URL environment variable not found")
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize the database with the Flask app
    db.init_app(app)
    
    # Enable CORS for all routes, specify origins if needed
    CORS(app) 

    # Import and register blueprints (update path if needed)
    from .app import main as main_blueprint  # Ensure correct import path
    from .interview import bp as interview_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(interview_blueprint, url_prefix='/api/interview')
    #app.register_blueprint(interview, url_prefix='/api')

    # Create database tables if they don't exist
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully.")
        except Exception as e:
            print(f"Error creating database tables: {e}")

    return app

if __name__ == "__main__":
    app = create_app()
    
    # Print a message indicating the app is running
    print("Starting Flask app...")
    
    try:
        # Run the app on the specified port
        app.run(host='0.0.0.0', port=5000)  # Adjust port as needed
    except Exception as e:
        print(f"Error starting Flask app: {e}")
