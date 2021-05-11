from django import forms


class CheckoutForm(forms.Form):
    initials = forms.CharField(label='ФИО', max_length=260)
    address = forms.CharField(label='Адрес', max_length=260)
    phone = forms.CharField(label='Контактный номер', max_length=260)
