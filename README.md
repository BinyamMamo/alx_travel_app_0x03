# ALX Travel App 0x03 - Background Jobs with Celery

A Django REST API application for travel property listings with integrated Celery background task processing for email notifications.

## Features

- **Property Listings**: CRUD operations for travel property listings
- **Booking System**: Create and manage property bookings
- **Payment Integration**: Chapa payment gateway integration
- **Background Email Tasks**: Asynchronous email notifications using Celery
- **Email Notifications**: Booking confirmation emails sent automatically

## Technology Stack

- **Django 5.1.4**: Web framework
- **Django REST Framework**: API development
- **Celery 5.4.0**: Background task processing
- **RabbitMQ**: Message broker (recommended)
- **Redis**: Result backend
- **SQLite**: Database (development)

## Setup Instructions

### 1. Clone and Install Dependencies

```bash
git clone <repository-url>
cd alx_travel_app_0x03
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment

Copy and configure the environment file:

```bash
cp .env.example .env
```

Update the `.env` file with your settings:
- `DEBUG`: Set to True for development
- `DATABASE_URL`: Database connection string
- `CHAPA_SECRET_KEY`: Your Chapa API secret key
- `CELERY_BROKER_URL`: RabbitMQ connection URL
- `EMAIL_HOST_USER`: Your email credentials

### 3. Set Up Message Broker

**Option A: RabbitMQ (Recommended)**
```bash
# Ubuntu/Debian
sudo apt-get install rabbitmq-server
sudo systemctl start rabbitmq-server
sudo systemctl enable rabbitmq-server
```

**Option B: Redis (Alternative)**
```bash
# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

### 4. Run Database Migrations

```bash
python manage.py migrate
```

### 5. Start the Services

**Terminal 1: Django Development Server**
```bash
source venv/bin/activate
python manage.py runserver
```

**Terminal 2: Celery Worker**
```bash
source venv/bin/activate
celery -A alx_travel_app worker --loglevel=info
```

Alternatively, use the provided script:
```bash
./start_celery_worker.sh
```

## Testing the Email System

### 1. Test Email Task Directly

```bash
python test_booking_email.py
```

### 2. Test with Celery Worker

```bash
python manage.py test_celery_email
```

### 3. Test via API

Create a booking via the API endpoint and observe the email being sent:

```bash
curl -X POST http://localhost:8000/api/bookings/ \
  -H "Content-Type: application/json" \
  -d '{
    "property_id": "your-property-uuid",
    "user_id": 1,
    "start_date": "2025-07-15",
    "end_date": "2025-07-17",
    "total_price": "300.00"
  }'
```

## API Endpoints

- `GET /api/listings/` - List all properties
- `POST /api/listings/` - Create a new property
- `GET /api/bookings/` - List all bookings
- `POST /api/bookings/` - Create a new booking (triggers email)
- `POST /api/payment/initiate/` - Initiate payment
- `GET /api/payment/verify/<tx_ref>/` - Verify payment

## Background Tasks

### Booking Confirmation Email

When a new booking is created, the system automatically:

1. Creates the booking record
2. Triggers `send_booking_confirmation_email.delay()` task
3. Celery worker processes the task asynchronously
4. Email is sent to the user with booking details

### Payment Confirmation Email

When a payment is verified, the system:

1. Updates payment status
2. Triggers `send_payment_email.delay()` task
3. Sends payment confirmation email

## Configuration Details

### Celery Settings

```python
CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
```

### Email Settings

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Development
EMAIL_HOST = 'smtp.gmail.com'  # Production
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

## Development Notes

- The application uses console email backend for development (emails appear in terminal)
- SQLite database is used for development
- RabbitMQ with Redis result backend is the recommended production setup
- All email tasks are configured as Celery shared tasks

## Troubleshooting

1. **Celery worker not starting**: Ensure RabbitMQ/Redis is running
2. **Import errors**: Check virtual environment activation
3. **Email not sending**: Verify email backend configuration
4. **Task not executing**: Check Celery worker logs

## Project Structure

```
alx_travel_app_0x03/
├── alx_travel_app/
│   ├── __init__.py           # Celery app initialization
│   ├── celery.py            # Celery configuration
│   ├── settings.py          # Django settings with Celery config
│   └── listings/
│       ├── tasks.py         # Background email tasks
│       ├── views.py         # API views with task triggers
│       └── models.py        # Database models
├── requirements.txt         # Python dependencies
├── test_booking_email.py    # Email task testing script
└── start_celery_worker.sh   # Celery worker startup script
```