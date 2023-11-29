#!/bin/bash

# NOTE: This script is not ran by default for the template docker image.
#       If you use a custom base image you can add your required system dependencies here.

set -e # Stop script on error
apt-get update && apt-get upgrade -y # Update System

# Install Poetry
python3.10 -m pip install poetry==1.7.1
poetry config virtualenvs.create false

# Clean up, remove unnecessary packages and help reduce image size
apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
