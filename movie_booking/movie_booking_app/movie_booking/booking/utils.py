from django.core.mail import send_mail
from django.conf import settings

def send_ticket_email(user_email, movie_title, show_time, seat_number, quantity):
    subject = f"Your Movie Ticket for {movie_title}"
    message = (
        f"Dear Customer,\n\n"
        f"Your ticket has been successfully booked.\n"
        f"Movie: {movie_title}\n"
        f"Show Time: {show_time}\n"
        f"Seat Number: {seat_number}\n"
        f"Quantity: {quantity}\n\n"
        f"Enjoy your movie!\n"
        f"Best regards,\n"
        f"Movie Booking Team"
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )
