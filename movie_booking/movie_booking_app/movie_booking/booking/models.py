from django.contrib.auth.models import User
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100, default="Unknown")
    release_date = models.DateField()
    poster = models.ImageField(upload_to='movie_posters/', null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    # New field

    def __str__(self):
        return self.title

from django.db import models

class ShowTime(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='show_times')
    show_time = models.TimeField()

    def __str__(self):
        return f"{self.movie.title} - {self.show_time.strftime('%I:%M %p')}"
 # Formats time

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    show_time = models.ForeignKey(ShowTime, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    seat_number = models.CharField(max_length=10, null=True, blank=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)  # ✅ Ensure this field is present

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} - Seat: {self.seat_number} - {'Paid' if self.is_paid else 'Pending'}"

class Payment(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Ticket {self.ticket.id} - {self.status}"
