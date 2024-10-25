from __init__ import db

class Interview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_position = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String(50), nullable=False)
    experience = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            "interviewId": self.id,
            "jobPosition": self.job_position,
            "jobDescription": self.job_description,
            "location": self.location,
            "salary": self.salary,
            "experience": self.experience,
        }
