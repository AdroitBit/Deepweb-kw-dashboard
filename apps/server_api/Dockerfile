# Use an official Python runtime as the base image
FROM python:3.11-alpine

RUN apk add build-base linux-headers

# Set the working directory in the container
WORKDIR /app



COPY ./requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt


# Copy the rest of the application code into the container
COPY ./ /app/

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run your application
CMD ["python3","-u", "server.py"]
