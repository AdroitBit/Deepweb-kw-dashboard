# Use an official Python runtime as the base image
FROM python:3.10-slim
FROM ubuntu:latest

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY ./src/requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY ./src/ /app/

# Expose the port the app runs on
EXPOSE 8080

# Define the command to run your application
CMD ["python", "main.py"]
