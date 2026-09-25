from django.conf import settings
from django.db import models
from django.utils import timezone


class Room(models.Model):
    number = models.CharField(max_length=10, unique=True)
    capacity = models.PositiveIntegerField()
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='rooms/', blank=True)

    def __str__(self):
        return f"Кімната {self.number}"


class Booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='bookings',
    )
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-check_in']

    def __str__(self):
        return f"{self.room} ({self.check_in} — {self.check_out})"

    def can_cancel(self):
        return self.check_in >= timezone.localdate()
