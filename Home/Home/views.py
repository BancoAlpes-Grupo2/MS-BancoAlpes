from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.middleware.csrf import get_token

import requests

from Home.forms import userForm

def home(request):
    return render(request, 'home.html')

def userFormView(request):
    if request.method == 'POST':
        form = userForm(request.POST)
        if form.is_valid():
            csrf_token = get_token(request)
            apiGateway = 'http://localhost:8000/auth/create/'
            response = requests.post(apiGateway, json=form.cleaned_data, headers={'X-CSRFToken': csrf_token}, cookies={'csrftoken': csrf_token})
            if response.status_code == 201:
                return redirect('home')
            else:
                return JsonResponse({"error": "Error al crear el usuario"}, status=400)
    return render(request, 'userForm.html')