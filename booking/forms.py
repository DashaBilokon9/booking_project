from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in', 'check_out']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, room=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = room

    def clean(self):
        cleaned = super().clean()
        check_in = cleaned.get('check_in')
        check_out = cleaned.get('check_out')
        if not check_in or not check_out:
            return cleaned

        if check_out <= check_in:
            raise ValidationError('Дата виїзду має бути пізніше заїзду.')
        if check_in < timezone.localdate():
            raise ValidationError('Не можна бронювати в минулому.')

        overlap = Booking.objects.filter(
            room=self.room,
            check_in__lt=check_out,
            check_out__gt=check_in,
        )
        if overlap.exists():
            raise ValidationError('Ця кімната вже зайнята на ці дати.')

        return cleaned
