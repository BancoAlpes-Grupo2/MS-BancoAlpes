from django import forms

from Users.models import User, UserAuth, UserCredentials

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'lastName', 'country', 'city', 'phone', 'email']

class UserAuthForm(forms.ModelForm):
    class Meta:
        model = UserAuth
        fields = ['name', 'lastName', 'country', 'city', 'phone', 'email', 'username', 'password', 'role']
        
class CredentialsForm(forms.ModelForm):
    class Meta:
        model = UserCredentials 
        fields = ['username', 'password', 'role']