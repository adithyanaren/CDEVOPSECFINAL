from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Movie, Ticket, ShowTime, Payment
from .forms import TicketForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'booking/movie_list.html', {'movies': movies})


from .utils import send_ticket_email

@login_required
def book_ticket(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    show_times = ShowTime.objects.filter(movie=movie)

    if request.method == "POST":
        show_time_id = request.POST.get("show_time")
        show_time = get_object_or_404(ShowTime, id=show_time_id)
        quantity = int(request.POST.get("quantity", 1))
        seat_number = request.POST.get("seat_number")

        # Check if the seat is already booked for the selected movie and show time
        existing_ticket = Ticket.objects.filter(
            movie=movie,
            show_time=show_time,
            seat_number=seat_number
        ).exists()

        if existing_ticket:
            return HttpResponse(
                "This seat is already booked. Please select a different seat.",
                status=400
            )

        # Create the ticket
        ticket = Ticket.objects.create(
            user=request.user,
            movie=movie,
            show_time=show_time,
            quantity=quantity,
            seat_number=seat_number,
            is_paid=False
        )

        # Send ticket confirmation email
        send_ticket_email(
            user_email=request.user.email,
            movie_title=movie.title,
            show_time=show_time.show_time.strftime('%I:%M %p'),
            seat_number=seat_number,
            quantity=quantity
        )

        return redirect("payment", ticket_id=ticket.id)

    return render(request, "booking/book_ticket.html", {"movie": movie, "show_times": show_times})



@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'booking/ticket_list.html', {'tickets': tickets})


@login_required
def ticket_update(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    if request.method == "POST":
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('ticket_list')
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'booking/book_ticket.html', {'form': form})


@login_required
def ticket_delete(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    if request.method == "POST":
        ticket.delete()
        return redirect('ticket_list')
    return render(request, 'booking/ticket_delete.html', {'ticket': ticket})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def payment_page(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    try:
        # Ensure only one payment per ticket and update the amount dynamically
        payment, created = Payment.objects.get_or_create(
            ticket=ticket,
            defaults={"amount": ticket.movie.price * ticket.quantity, "status": "Pending"}
        )

        # If the payment already exists, update the amount
        if not created:
            payment.amount = ticket.movie.price * ticket.quantity
            payment.save()

    except Exception as e:
        return HttpResponse(f"Unexpected error: {str(e)}", status=500)

    if request.method == "POST":
        # Mark payment as completed
        payment.status = "Completed"
        payment.save()
        return redirect("success", ticket_id=ticket.id)

    return render(request, "booking/payment.html", {"ticket": ticket, "payment": payment})


@login_required
def payment_success(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    payment = get_object_or_404(Payment, ticket=ticket)

    return render(request, 'booking/success.html', {
        'ticket': ticket,
        'payment': payment,  # Pass the payment object to the template
    })

