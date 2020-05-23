from django import forms
import datetime


class ReservationDayForm(forms.Form):
    checkin = forms.DateField(
        initial=datetime.date.today, label='Check-in', input_formats=['%d/%m/%Y'])
    days = forms.IntegerField(label='Days', min_value=1)
