from django import forms

class CheckoutForm(forms.Form):
    initials = forms.CharField(label='ФИО', max_length=260)
    adress = forms.CharField(label='Адрес', max_length=260)