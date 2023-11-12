# Use the official Python image as a parent image
FROM python:3

# Set the working directory in the container
WORKDIR /usr/src/voice_automatisation

# Copy your Python project files to the container
COPY src/ .
RUN apt-get update && apt-get install -y portaudio19-dev
RUN apt-get install -y alsa-utils
RUN pip install -r requirements.txt

# Specify the command to run your Python application
CMD ["python", "main.py"]
