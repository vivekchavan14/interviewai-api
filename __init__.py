from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configure the database
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize the database with the app
    db.init_app(app)

    # Import and register blueprints (if any)
    from .app import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Create database tables if they don't exist
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Error creating database tables: {e}")

    return app

if __name__ == "__main__":
    app = create_app()
    
    # Print a statement indicating the app is running
    print("Starting Flask app...")
    
    try:
        # Run the app on the specified port
        app.run(host='0.0.0.0', port=5000)  # Change port if necessary
    except Exception as e:
        print(f"Error starting Flask app: {e}")
