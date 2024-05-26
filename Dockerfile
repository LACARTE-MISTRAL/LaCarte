# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create and set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install system dependencies and Python packages in a single RUN command
RUN apt-get update && apt-get install -y \
    build-essential \
    qt5-qmake \
    qtbase5-dev \
    libqt5webkit5-dev \
    libqt5svg5-dev \
    libqt5webengine-data \
    libqt5webengine5 \
    libqt5webenginewidgets5 \
    libxcb-xinerama0 && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the rest of the application code into the container
COPY . /app/

# Expose the port the app runs on
EXPOSE 4242

# Command to run the application
CMD ["flask", "--app", "application.py", "--debug", "run", "--host", "0.0.0.0"]