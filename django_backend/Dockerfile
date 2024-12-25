FROM python:3.12.2-slim-bullseye

# Set the working directory
WORKDIR /usr/src/django_backend

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies for OpenCV, Tesseract, and YOLO
RUN apt-get update && apt-get install -y \
    wget \
    netcat \
    build-essential \
    cmake \
    libgtk2.0-dev \
    pkg-config \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libxvidcore-dev \
    libx264-dev \
    gfortran \
    libatlas-base-dev \
    tesseract-ocr \
    && apt-get clean

# Download the Khmer.traineddata file
RUN wget -P /usr/share/tesseract-ocr/4.00/tessdata/ https://github.com/tesseract-ocr/tessdata/raw/main/script/Khmer.traineddata

# Set the TESSDATA_PREFIX environment variable
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements file and install Python dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install pytesseract and ultralytics
RUN pip install --no-cache-dir pytesseract ultralytics

# Create media directory
RUN mkdir -p /usr/src/django_backend/media

# Copy the entrypoint script and make it executable
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/django_backend/entrypoint.sh
RUN chmod +x /usr/src/django_backend/entrypoint.sh

# Copy the entire project into the container
COPY . .

# Set the entrypoint
ENTRYPOINT [ "/usr/src/django_backend/entrypoint.sh" ]
