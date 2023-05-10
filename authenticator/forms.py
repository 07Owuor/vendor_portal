from django import forms


class LoginForm(forms.Form):
    email_address = forms.CharField(required=True, widget=forms.EmailField)
    password = forms.CharField(required=True, widget=forms.PasswordInput)