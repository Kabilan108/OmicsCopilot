FROM python:3.10.13-slim

# Set working dir inside container
WORKDIR /server

# Install system dependencies
ENV TZ=America/New_York
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    libopencv-dev \
    tesseract-ocr \
    libtesseract-dev \
    git \
    curl \
    tzdata \
    && apt-get -y upgrade \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install --upgrade pip \
    && pip install poetry==1.7.1

# Copy poetry files
COPY poetry.lock pyproject.toml ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi
    # --only main

# Expose port 8000
EXPOSE 8000

# Copy source code
# COPY . .

# Run the server
# RUN chmox +x ./run_server.sh
# CMD ["./run_server.sh"]
