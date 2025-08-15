#!/bin/sh
# Abort on any error
set -e

# Start the main application
echo "Starting the application..."
exec "$@"
