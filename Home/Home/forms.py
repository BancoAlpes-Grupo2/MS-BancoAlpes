from django import forms

from Home.models import Credentials, User

class userForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'lastName', 'country', 'city', 'phone', 'email', 'username', 'password']

class CredentialsForm(forms.ModelForm):
    class Meta:
        model = Credentials
        fields = ['username', 'password']