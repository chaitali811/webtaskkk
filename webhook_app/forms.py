from django import forms
from .models import Account, Destination


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'account_name', 'website']


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['account', 'url', 'http_method', 'headers']
