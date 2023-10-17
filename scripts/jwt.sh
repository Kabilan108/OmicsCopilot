#!/bin/bash

# This script generates a new secret key for the JWT tokens

# Generate a new secret key using Python
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")

# Check if the line already exists
if grep -q "SECRET_KEY=" ".env"; then
    # If it exists, replace it
    sed -i "s/SECRET_KEY=.*/SECRET_KEY=\"$SECRET_KEY\"/" .env
else
    # If not, add it to the file
    echo "SECRET_KEY=\"$SECRET_KEY\"" >> .env
fi

echo "Updated .env with new SECRET_KEY."
