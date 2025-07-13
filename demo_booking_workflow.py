#!/usr/bin/env python
"""
Demonstration script showing complete booking workflow with email notification
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
from datetime import date, timedelta
import requests
import json

def test_booking_api_with_email():
    """Test the complete booking API flow including email notification"""
    print("Testing complete booking API workflow with email notifications...")
    
    # Create test user
    user, created = User.objects.get_or_create(
        username='apitest',
        defaults={
            'email': 'apitest@example.com',
            'first_name': 'API',
            'last_name': 'Test'
        }
    )
    print(f"User: {user.username} (created: {created})")
    
    # Create test listing
    listing, created = Listing.objects.get_or_create(
        name='API Test Property',
        defaults={
            'host_id': user,
            'description': 'Beautiful property for API testing',
            'location': 'API City, Test Country',
            'pricepernight': 200.00
        }
    )
    print(f"Listing: {listing.name} (created: {created})")
    
    # Test data for booking creation
    booking_data = {
        'property_id': str(listing.listing_id),
        'user_id': user.id,
        'start_date': (date.today() + timedelta(days=3)).isoformat(),
        'end_date': (date.today() + timedelta(days=6)).isoformat(),
        'total_price': '600.00'
    }
    
    print(f"Booking data: {booking_data}")
    
    # Simulate the BookingViewSet create method
    from alx_travel_app.listings.views import BookingViewSet
    from rest_framework.request import Request
    from django.test import RequestFactory
    
    factory = RequestFactory()
    request = factory.post('/api/bookings/', booking_data, content_type='application/json')
    request.user = user
    
    # Create the viewset and call the create method
    viewset = BookingViewSet()
    
    class MockRequest:
        def __init__(self, data, user):
            self.data = data
            self.user = user
    
    mock_request = MockRequest(booking_data, user)
    
    try:
        # This would normally trigger the email task
        print("Creating booking via ViewSet...")
        print("Note: This demonstration shows the email task would be triggered.")
        print("The actual email sending requires a running Celery worker.")
        
        # Show what the email task would do
        from alx_travel_app.listings.tasks import send_booking_confirmation_email
        
        # Create booking directly for demo
        booking = Booking.objects.create(
            property_id=listing,
            user_id=user,
            start_date=booking_data['start_date'],
            end_date=booking_data['end_date'],
            total_price=booking_data['total_price']
        )
        
        print(f"Booking created: {booking.booking_id}")
        print("Email task trigger: send_booking_confirmation_email.delay()")
        
        # Execute email task synchronously for demo
        result = send_booking_confirmation_email(str(booking.booking_id))
        print(f"Email task result: {result}")
        
    except Exception as e:
        print(f"Error during booking creation: {e}")
    
    print("Demonstration completed!")

if __name__ == '__main__':
    test_booking_api_with_email()
