#!/bin/bash
# Initialize and run the Telegram userbot.

set -e

echo "Initializing Telegram userbot..."

source ../.env

# Check if required environment variables are set
if [ -z "$TG_API_ID" ] || [ -z "$TG_API_HASH" ]; then
    echo "Error: TG_API_ID and TG_API_HASH must be set in the environment variables."
    exit 1
fi

echo "Generating userbot session key..."
python ../telega/generate_session.py

echo "Starting userbot..."
python ../telega/bot/main.py