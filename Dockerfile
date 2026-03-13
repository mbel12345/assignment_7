# Use the official Python image from DockerHub, with minimal dependencies to reduce attack surface
FROM python:3.12-slim-bullseye

# Set the working directory inside the container
WORKDIR /app

# Install system libraries required for python dependencies to work
RUN apt-get update && apt-get install -y \
    libfreetype6-dev \
    libjpeg62-turbo-dev \
    libpng-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Create the dirs for logs and QR codes, and set ownership to non-root user, which helps with security.
RUN useradd -m myuser && mkdir logs qr_codes && chown myuser:myuser logs qr_codes

# Copy the rest of the application's source code into the container, setting ownership to 'myuser'
COPY --chown=myuser:myuser . .

# Switch to the non-root user for security
USER myuser

# Use ENTRYPOINT and CMD to allow flexibility when running the container
ENTRYPOINT ["python", "main.py"]
CMD ["--url", "https://hub.docker.com/repository/docker/msb64/qr-code-generator-app/general"]
