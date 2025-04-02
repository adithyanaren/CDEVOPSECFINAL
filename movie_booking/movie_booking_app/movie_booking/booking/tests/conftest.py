import pytest
from django.contrib.auth.models import User
from booking.models import Movie, Ticket, ShowTime

@pytest.fixture
def test_user(db):
    return User.objects.create_user(username='testuser', password='testpassword')

@pytest.fixture
def test_movie(db):
    return Movie.objects.create(
        title='Test Movie',
        genre='Action',
        release_date='2023-01-01'
    )

@pytest.fixture
def test_showtime(db, test_movie):
    return ShowTime.objects.create(
        movie=test_movie,
        show_time='15:30:00'
    )

@pytest.fixture
def test_ticket(db, test_user, test_movie, test_showtime):
    return Ticket.objects.create(
        user=test_user,
        movie=test_movie,
        show_time=test_showtime,
        seat_number='A1'
    )
