# Use an official Python runtime as the base image
FROM python:3.11-alpine
# FROM ubuntu:latest

# Set the working directory in the container
WORKDIR /app


# Copy the rest of the application code into the container
COPY ./src /app/

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt



# Expose the port the app runs on
EXPOSE 5000

# Define the command to run your application
CMD ["python3", "server.py"]
