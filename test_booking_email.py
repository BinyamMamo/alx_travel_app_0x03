#!/usr/bin/env python
"""
Test script to verify booking email functionality
"""
import os
import sys
import django
from django.conf import settings

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app.settings')
django.setup()

from alx_travel_app.listings.models import Listing, Booking
from django.contrib.auth.models import User
from alx_travel_app.listings.tasks import send_booking_confirmation_email
from datetime import date, timedelta
import uuid

def test_booking_email():
    """Test the booking confirmation email task"""
    print("Testing booking confirmation email task...")
    
    # Create a test user if it doesn't exist
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    if created:
        print(f"Created test user: {user.username}")
    else:
        print(f"Using existing test user: {user.username}")
    
    # Create a test listing if it doesn't exist
    listing, created = Listing.objects.get_or_create(
        name='Test Property',
        defaults={
            'host_id': user,
            'description': 'A beautiful test property',
            'location': 'Test City, Test Country',
            'pricepernight': 100.00
        }
    )
    
    if created:
        print(f"Created test listing: {listing.name}")
    else:
        print(f"Using existing test listing: {listing.name}")
    
    # Create a test booking
    booking = Booking.objects.create(
        property_id=listing,
        user_id=user,
        start_date=date.today() + timedelta(days=1),
        end_date=date.today() + timedelta(days=3),
        total_price=200.00
    )
    
    print(f"Created test booking: {booking.booking_id}")
    
    # Test the email task directly (synchronously for testing)
    result = send_booking_confirmation_email(str(booking.booking_id))
    print(f"Email task result: {result}")
    
    # Clean up
    booking.delete()
    print("Test completed and cleaned up!")

if __name__ == '__main__':
    test_booking_email()
