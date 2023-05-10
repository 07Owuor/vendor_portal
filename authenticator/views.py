from django.shortcuts import render
from .forms import LoginForm

# Create your views here.


def login_user(request):
    template_name = "auth/login.html"
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
            email_address = str(str(form.cleaned_data['email_address']))
            password = str(str(form.cleaned_data['password']))
            payload = {
                "email": email_address,
                "password": password
            }
    return render(request, template_name)