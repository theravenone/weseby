from django import forms

class LakiForm(forms.Form):
    """ Form for Laki Input """
    vorname = forms.CharField(label='Vorname:', max_length=20)


class KioskForm(forms.Form):
    """ Form for Kiosk Buttons """
    betrag = forms.CharField()

class ManualForm(forms.Form):
    """ Form for manual calculation """
    amount = forms.DecimalField(max_digits=5, decimal_places=2)
