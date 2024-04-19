# Use an official Python runtime as the base image
FROM python:3.11-alpine


ENV URL_PROCESS_CHUNK_SIZE 10
ENV KEYWORDS "kasetsart, ku.th, ku.ac.th, ku.th, @ku.ac.th, @ku.th, drug, porn, sex"
ENV CHECKING_URLS_LIMIT 100000
# FROM ubuntu:latest

# Set the working directory in the container
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
# Copy the rest of the application code into the container
COPY ./ .

# Install dependencies



# Expose the port the app runs on
EXPOSE 5050

# Define the command to run your application
CMD ["python3","-u", "main.py"]
