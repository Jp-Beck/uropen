# Set base image
FROM python:3.9.6-alpine

# Set working directory in the container
WORKDIR /app

# Copy requirements.txt to the container
COPY openur/requirements.txt .

# Install dependencies in the container
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY openur/ .

