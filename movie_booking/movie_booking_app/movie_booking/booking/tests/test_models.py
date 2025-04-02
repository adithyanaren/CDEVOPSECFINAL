def test_movie_creation(test_movie):
    assert test_movie.title == 'Test Movie', "Movie title mismatch"

def test_ticket_creation(test_ticket):
    assert test_ticket.seat_number == 'A1', "Seat number mismatch"
    assert test_ticket.user.username == 'testuser', "User mismatch"
