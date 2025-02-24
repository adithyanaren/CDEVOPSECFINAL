from django.urls import path
from django.contrib.auth import views as auth_views  # Import Django's built-in auth views
from . import views  # Import the whole views module
from django.conf import settings
from django.conf.urls.static import static
from .views import payment_page, payment_success

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('movie_list/', views.movie_list, name='movie_list'),
    path('book/<int:movie_id>/', views.book_ticket, name='book_ticket'),
    path('tickets/', views.ticket_list, name='ticket_list'),
    path('tickets/update/<int:ticket_id>/', views.ticket_update, name='ticket_update'),
    path('tickets/delete/<int:ticket_id>/', views.ticket_delete, name='ticket_delete'),

    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='movie_list'), name='logout'),
    path("payment/<int:ticket_id>/", payment_page, name="payment"),
    path("success/<int:ticket_id>/", payment_success, name="success"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
