from django import forms

from Home.models import User

class userForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'lastName', 'country', 'city', 'phone', 'email', 'username', 'password']