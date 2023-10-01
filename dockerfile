# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM ubuntu:latest

# Set the working directory in docker
WORKDIR /app

# Copy local code to the container image.
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

# Install production dependencies.
RUN pip3 install --no-cache-dir fastapi[all] curl_cffi uvicorn

# Specify the command to run on container start
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
