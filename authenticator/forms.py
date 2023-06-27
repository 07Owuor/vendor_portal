from django import forms


class LoginForm(forms.Form):
    email_address = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'type': 'email',
        'class': 'form-control form-control-user',
        'placeholder': 'Enter your email address'
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'type': 'password',
        'class': 'form-control form-control-user',
        'placeholder': 'Enter your email password'
    }))