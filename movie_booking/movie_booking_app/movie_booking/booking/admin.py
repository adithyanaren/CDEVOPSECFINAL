from django.contrib import admin
from .models import Movie, Ticket, ShowTime

admin.site.register(Movie)
admin.site.register(Ticket)
admin.site.register(ShowTime)  # Ensure this line exists
