from django.urls import reverse

def test_login_view(client, test_user):
    response = client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 302, "Login failed"
    assert response.url == reverse('movie_list'), "Did not redirect to movie list"

def test_logout_view(client, test_user):
    client.login(username='testuser', password='testpassword')
    response = client.get(reverse('logout'))
    assert response.status_code == 302, "Logout failed"
