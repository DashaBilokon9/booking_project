from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import BookingForm
from .models import Booking, Room


def home(request):
    rooms = Room.objects.order_by('number')
    return render(request, 'booking/home.html', {'rooms': rooms})


@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if request.method == 'POST':
        form = BookingForm(request.POST, room=room)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.save()
            messages.success(request, f'Кімнату {room.number} заброньовано.')
            return redirect('my_bookings')
    else:
        form = BookingForm(room=room)

    return render(request, 'booking/book_room.html', {'form': form, 'room': room})


@login_required
def my_bookings(request):
    bookings = (
        Booking.objects.filter(user=request.user)
        .select_related('room')
        .order_by('-check_in')
    )
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})


@login_required
@require_POST
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    if not booking.can_cancel():
        messages.error(request, 'Минуле бронювання скасувати не можна.')
        return redirect('my_bookings')

    booking.delete()
    messages.success(request, 'Бронювання скасовано. Кімната знову вільна на ці дати.')
    return redirect('my_bookings')
