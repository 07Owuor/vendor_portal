from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from .forms import LoginForm
import requests

# Create your views here.

User = get_user_model()


def login_user(request):
    template_name = "auth/login.html"
    error_message = ""
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
            email_address = str(str(form.cleaned_data['email_address']))
            password = str(str(form.cleaned_data['password']))
            print(password, email_address)
            data = {
                "params": {
                    "login": email_address,
                    "password": password,
                    "db": "saner-gy-sanergy-dev-2-8930226"
                }
            }
            response = requests.get('https://odoo.develop.saner.gy/web/session/authenticate', json=data)
            try:
                if response.status_code == 200:
                    # Authentication successful
                    user_response = response.json()

                    user_data = user_response['result']

                    # Check if the user already exists in your Django database
                    try:
                        user = User.objects.get(email=email_address)
                    except User.DoesNotExist:
                        # Create a new user if not found
                        user = User.objects.create_user(email=email_address, password=password)

                    # Retrieve the access token from the API response
                    partner_id = user_data['partner_id']
                    user_name = user_data['partner_display_name']
                    company_id = user_data['company_id']

                    if int(company_id) == 1:
                        company = "Regen Organics"
                    elif int(company_id) == 2:
                        company = "Fresh Life LTD"
                    else:
                        company = "Sanergy Collaborative"
                    user.first_name = user_name
                    user.save()

                    # Store the access token in the session
                    request.session['partner_id'] = partner_id
                    request.session['user_name'] = user_name
                    request.session['company'] = company
                    request.session['company_id'] = company_id
                    header = str(response.headers['Set-Cookie']).split(';')
                    print(header)
                    request.session['session_id'] = header[0]
                    login(request, user)
                    return redirect('home')

            except Exception as e:
                error_message = str(e)
                print(e)

    else:
        form = LoginForm

    data = {
        'form': form,
        'error_message': error_message
    }

    return render(request, template_name, data)


def logout_user(request):
    try:
        del request.session['partner_id']
        del request.session['session_id']
    except Exception as e:
        print(str(e))
        pass

    return redirect('login')