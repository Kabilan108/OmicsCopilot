# Use official NVIDIA runtime with cuDNN
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Set working dir inside container
WORKDIR /server

# Install system dependencies
ENV TZ=America/New_York
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    python3-pip \
    python3-dev \
    libopencv-dev \
    tesseract-ocr \
    libtesseract-dev \
    git \
    curl \
    tzdata \
    && apt-get -y upgrade \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

# Ensure that the default python is set to Python 3.10
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1

# Make sure we use the correct pip version
RUN ln -s $(which pip3) /usr/local/bin/pip

# Install poetry
RUN pip install --upgrade pip \
    && pip install poetry==1.7.1

# Copy poetry files
COPY poetry.lock pyproject.toml ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Expose port 8000
EXPOSE 8000

# Download and optimize models
CMD ["./scripts/download_models.sh"]

# Copy source code
# COPY . .

# Run the server
# RUN chmox +x ./run_server.sh
# CMD ["./run_server.sh"]
