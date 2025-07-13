from celery import shared_task
from .models import Payment, Booking
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_payment_email(transaction_id):
    """Send payment confirmation email"""
    payment = Payment.objects.get(transaction_id=transaction_id)
    user = payment.booking_id.user_id
    send_mail(
        'Payment Confirmation',
        f'Your payment of {payment.amount} ETB has been received.',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

@shared_task
def send_booking_confirmation_email(booking_id):
    """Send booking confirmation email to user"""
    try:
        booking = Booking.objects.get(booking_id=booking_id)
        user = booking.user_id
        property_name = booking.property_id.name
        
        subject = 'Booking Confirmation - ALX Travel App'
        message = f'''
Dear {user.first_name or user.username},

Your booking has been successfully created!

Booking Details:
- Property: {property_name}
- Location: {booking.property_id.location}
- Check-in: {booking.start_date}
- Check-out: {booking.end_date}
- Total Price: {booking.total_price} ETB
- Booking ID: {booking.booking_id}

Thank you for choosing ALX Travel App!

Best regards,
The ALX Travel Team
        '''
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        
        return f"Booking confirmation email sent to {user.email}"
        
    except Booking.DoesNotExist:
        return f"Booking with ID {booking_id} not found"
    except Exception as e:
        return f"Error sending booking confirmation email: {str(e)}"