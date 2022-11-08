from django import forms

class UserForm(forms.Form):
    username = forms.CharField(label='username', max_length=255)
    password = forms.CharField(label='password', max_length=255)
    email = forms.CharField(label='email', max_length=255)
    role = forms.CharField(label='role', max_length=255)