from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.middleware.csrf import get_token

import requests

from Home.forms import CredentialsForm, userForm
from Home.utils.authentication import jwt_optional

@jwt_optional
def home(request):
    user = None
    if hasattr(request, 'user_id'):
        user = requests.get(f'http://localhost:8000/users/{request.user_id}/', cookies={'authToken': request.COOKIES.get('authToken')}).json()
    if request.method == 'POST':
        if not user:
            form = CredentialsForm(request.POST)
            if form.is_valid():
                csrf_token = get_token(request)
                apiGateway = 'http://localhost:8000/auth/'
                response = requests.post(apiGateway, json=form.cleaned_data, headers={'X-CSRFToken': csrf_token}, cookies={'csrftoken': csrf_token})
                if response.status_code == 200:
                    token = response.cookies.get('authToken')
                    response = redirect('home')
                    response.set_cookie('authToken', token)
                    return response
                else:
                    return JsonResponse({"error": "Error al iniciar sesión"}, status=400)
        else:
            response = redirect('home')
            response.delete_cookie('authToken')
            return response
    return render(request, 'home.html', context={'user': user})

def userFormView(request):
    if request.method == 'POST':
        form = userForm(request.POST)
        if form.is_valid():
            csrf_token = get_token(request)
            apiGateway = 'http://localhost:8000/auth/create/'
            data = form.cleaned_data
            data['role'] = 'user'
            response = requests.post(apiGateway, json=data, headers={'X-CSRFToken': csrf_token}, cookies={'csrftoken': csrf_token})
            if response.status_code == 201:
                token = response.cookies.get('authToken')
                response = redirect('home')
                response.set_cookie('authToken', token)
                return response
    return render(request, 'userForm.html')