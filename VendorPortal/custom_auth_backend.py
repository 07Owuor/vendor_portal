from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
import requests

User = get_user_model()


class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Make a request to the external API for user authentication
        response = requests.post('https://portal.saner.gy/auth/login', data={
            'email': username,
            'password': password
        })

        if response.status_code == 201:
            # Authentication successful
            user_response = response.json()

            user_data = user_response['data']

            # Check if the user already exists in your Django database
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                # Create a new user if not found
                user = User.objects.create_user(email=username, password=password)

            # Retrieve the access token from the API response
            access_token = user_data['accessToken']
            print(access_token)

            # Store the access token in the session
            request.session['access_token'] = access_token
            print(user)

            return user

        # Authentication failed
        return None
