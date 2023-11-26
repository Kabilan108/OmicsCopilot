#!/bin/bash

# Set the script to exit immediately if any command fails
set -e

# Define variables
API_RELOAD="${API_RELOAD:-false}"
API_HOST="${API_HOST:-localhost}"
API_PORT="${API_PORT:-8000}"

# Run the server
if [ "$API_RELOAD" = "true" ]; then
    echo "Running server with reload"
    uvicorn api.app:app --reload --host "$API_HOST" --port "$API_PORT"
else
    echo "Running server without reload"
    uvicorn api.app:app --host "$API_HOST" --port "$API_PORT"
fi
