# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set a working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .

# Install system dependencies for pyttsx3 (eSpeak) and other requirements
RUN apt-get update && \
    apt-get install -y espeak ffmpeg libespeak-ng1 && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the application port (adjust if not 5000)
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=__init__.py
ENV FLASK_RUN_HOST=0.0.0.0

# Command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
