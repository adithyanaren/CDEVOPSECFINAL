from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from booking.models import Movie, ShowTime, Ticket

class BookingViewsTest(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test movie
        self.movie = Movie.objects.create(
            title='Test Movie',
            release_date='2023-01-01',
            genre='Action'
        )

        # Create a test show time
        self.show_time = ShowTime.objects.create(
            movie=self.movie,
            show_time='18:00:00'
        )

        # Create a booking for the test movie and show time
        self.ticket = Ticket.objects.create(
            user=self.user,
            movie=self.movie,
            show_time=self.show_time,
            seat_number='A1'
        )

        # Instantiate the client
        self.client = Client()

    def test_movie_list_view(self):
        """Test if the movie list page loads correctly"""
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Movie')

    def test_ticket_list_view(self):
        """Test if the ticket list page loads correctly after login"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('ticket_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A1')

    def test_create_ticket_view(self):
        """Test ticket creation and redirection"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('book_ticket', args=[self.movie.id]), {
            'movie': self.movie.id,
            'show_time': self.show_time.id,
            'seat_number': 'B2'
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect after creation
        self.assertTrue(Ticket.objects.filter(seat_number='B2').exists())

    def test_login_required_for_ticket_list(self):
        """Test that ticket list page requires login"""
        response = self.client.get(reverse('ticket_list'))
        self.assertNotEqual(response.status_code, 200)  # Should redirect to login

    def test_login_view(self):
        """Test successful login"""
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('movie_list'))

    def test_logout_view(self):
        # Log in the user first
        self.client.login(username='testuser', password='testpassword')

        # Use POST method for logout since it is more secure
        response = self.client.post(reverse('logout'), follow=True)

        # Check if redirected to the movie list page after logout
        self.assertEqual(response.status_code, 200)  # Expected 200 after redirection
        self.assertContains(response, 'Login')  # Ensure the user is logged out

    def test_invalid_login(self):
        """Test login with invalid credentials"""
        response = self.client.post(reverse('login'), {'username': 'invaliduser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)  # Should stay on the login page
        self.assertContains(response, "Please enter a correct username and password.")

    def test_delete_ticket_view(self):
        """Test ticket deletion"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('ticket_delete', args=[self.ticket.id]))
        self.assertEqual(response.status_code, 302)  # Check for redirect after deletion
        self.assertFalse(Ticket.objects.filter(id=self.ticket.id).exists())

    def test_update_ticket_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        # Send a POST request to update the ticket
        response = self.client.post(reverse('ticket_update', args=[self.ticket.id]), {
            'movie': self.movie.id,
            'show_time': self.show_time.id,
            'seat_number': 'A2'
        })
        # Check for redirection after update (302)
        self.assertEqual(response.status_code, 302)
        # Check if the update was successful
        self.assertTrue(Ticket.objects.filter(seat_number='A2').exists())

    def test_movie_detail_view(self):
        # Log in the user before accessing the detail view
        self.client.login(username='testuser', password='testpassword')
        # Access the movie detail page
        response = self.client.get(reverse('book_ticket', args=[self.movie.id]))
        # Check for successful page load (200)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Movie')

