from django import forms

class LakiForm(forms.Form):
    vorname = forms.CharField(label='Vorname:', max_length=20)


class KioskForm(forms.Form):
    amount = forms.DecimalField(max_digits=5, decimal_places=2)