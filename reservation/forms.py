from django import forms


class ReservationDayForm(forms.Form):
    checkin = forms.DateField(label='Check-in', input_formats=['%d/%m/%Y'])
    days = forms.IntegerField(label='Days')
