#!/bin/sh
# Abort on any error
set -e

# Apply database migrations
echo "Applying database migrations..."
flask db upgrade

# Start the main application
echo "Starting the application..."
exec "$@"