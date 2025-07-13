#!/usr/bin/env python
"""
Management command to test Celery task functionality
"""
import os
import sys
import django
from django.core.management.base import BaseCommand

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app.settings')
django.setup()

from alx_travel_app.listings.models import Listing, Booking
from django.contrib.auth.models import User
from alx_travel_app.listings.tasks import send_booking_confirmation_email
from datetime import date, timedelta
import uuid

class Command(BaseCommand):
    help = 'Test the Celery booking email task'

    def handle(self, *args, **options):
        self.stdout.write("Testing Celery booking confirmation email task...")
        
        # Create a test user if it doesn't exist
        user, created = User.objects.get_or_create(
            username='celerytest',
            defaults={
                'email': 'celerytest@example.com',
                'first_name': 'Celery',
                'last_name': 'Test'
            }
        )
        
        if created:
            self.stdout.write(f"Created test user: {user.username}")
        else:
            self.stdout.write(f"Using existing test user: {user.username}")
        
        # Create a test listing if it doesn't exist
        listing, created = Listing.objects.get_or_create(
            name='Celery Test Property',
            defaults={
                'host_id': user,
                'description': 'A beautiful property for Celery testing',
                'location': 'Celery City, Test Country',
                'pricepernight': 150.00
            }
        )
        
        if created:
            self.stdout.write(f"Created test listing: {listing.name}")
        else:
            self.stdout.write(f"Using existing test listing: {listing.name}")
        
        # Create a test booking
        booking = Booking.objects.create(
            property_id=listing,
            user_id=user,
            start_date=date.today() + timedelta(days=2),
            end_date=date.today() + timedelta(days=5),
            total_price=450.00
        )
        
        self.stdout.write(f"Created test booking: {booking.booking_id}")
        
        # Test the email task asynchronously with delay()
        self.stdout.write("Sending email task to Celery worker...")
        result = send_booking_confirmation_email.delay(str(booking.booking_id))
        
        self.stdout.write(f"Task ID: {result.id}")
        self.stdout.write("Email task has been queued for processing by Celery worker.")
        self.stdout.write("Check the Celery worker output for the email content.")
        
        # Keep the booking for testing - don't clean up
        self.stdout.write("Test booking created successfully!")
