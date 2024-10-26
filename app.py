from flask import Blueprint, jsonify, request # type: ignore
from .models import db, Interview  

# Define the blueprint
main = Blueprint('main', __name__)

@main.route('/jobs', methods=['GET'])
def get_jobs():
    """Fetch all jobs from the database and return them as JSON."""
    try:
        jobs = Interview.query.all()
        return jsonify([job.to_dict() for job in jobs]), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch jobs: {e}"}), 500

@main.route('/jobs', methods=['POST'])
def add_job():
    """Add a new job to the database."""
    data = request.get_json()
    
    # Validate input data
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    
    required_fields = ['jobPosition', 'jobDescription', 'location', 'salary', 'experience']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Create a new job instance
        new_job = Interview(
            job_position=data['jobPosition'],
            job_description=data['jobDescription'],
            location=data['location'],
            salary=data['salary'],
            experience=data['experience']
        )
        
        # Add to the database and commit
        db.session.add(new_job)
        db.session.commit()
        
        return jsonify(new_job.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to add job: {e}"}), 500
