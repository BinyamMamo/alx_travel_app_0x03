#!/bin/bash

# Script to start Celery worker for ALX Travel App

echo "Starting Celery worker for ALX Travel App..."
echo "Make sure RabbitMQ is running before starting this worker."
echo "You can install RabbitMQ with: sudo apt-get install rabbitmq-server"
echo "And start it with: sudo systemctl start rabbitmq-server"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Start Celery worker
echo "Starting Celery worker..."
celery -A alx_travel_app worker --loglevel=info

echo "Celery worker stopped."
