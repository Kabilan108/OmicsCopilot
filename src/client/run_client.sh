#!/bin/bash

# Set the script to exit immediately if any command fails
set -e

# Define variables
CLIENT_HOST="${CLIENT_HOST:-localhost}"
CLIENT_PORT="${CLIENT_PORT:-3001}"
CLIENT_RELOAD="${CLIENT_RELOAD:-false}"

# Run the client
streamlit run app/home.py \
    --server.port "$CLIENT_PORT" \
    --server.address "$CLIENT_HOST" \
    --server.runOnSave "$CLIENT_RELOAD"
