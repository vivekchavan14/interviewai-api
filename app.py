from flask import Blueprint, jsonify, request
from models import db, Interview

main = Blueprint('main', __name__)

@main.route('/jobs', methods=['GET'])
def get_jobs():
    jobs = Interview.query.all()
    return jsonify([job.to_dict() for job in jobs]), 200

@main.route('/jobs', methods=['POST'])
def add_job():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    
    required_fields = ['jobPosition', 'jobDescription', 'location', 'salary', 'experience']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    new_job = Interview(
        job_position=data['jobPosition'],
        job_description=data['jobDescription'],
        location=data['location'],
        salary=data['salary'],
        experience=data['experience']
    )
    
    db.session.add(new_job)
    db.session.commit()
    return jsonify(new_job.to_dict()), 201
