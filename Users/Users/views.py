from django.http import JsonResponse
from rest_framework.decorators import api_view

from Users.forms import CredentialsForm, UserAuthForm, UserForm
from Users.models import User
from Users.utils.authentication import jwt_required
from django.http import HttpResponseRedirect

import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.middleware.csrf import get_token

@api_view(['POST'])
def createUser(request):
    form = UserForm(request.data)
    if form.is_valid():
        form.save()
        return JsonResponse({"message": "User created successfully"}, status=201)
    return JsonResponse({"error": "Form data is invalid", "details": form.errors}, status=400)

@api_view(['GET'])
@jwt_required
def getUsers(request):
    users = User.objects.all()
    users = [{"name": user.name, "lastName": user.lastName, "country": user.country, "city": user.city, "phone": user.phone, "email": user.email} for user in users]
    #print(request.user_id)
    #print(request.user_role)
    return JsonResponse(users, safe=False, status=200)

@api_view(['GET'])
@jwt_required
def getUser(request, userId):
    try:
        user = User.objects.get(pk=userId)
        userData = {
            "name": user.name,
            "lastName": user.lastName,
            "country": user.country,
            "city": user.city,
            "phone": user.phone,
            "email": user.email
        }
        print(request.user_id)
        print(request.user_role)
        return JsonResponse(userData, status=200)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

def home(request):
    url = f"{request.scheme}://{request.get_host()}/"
    return HttpResponseRedirect(url)

#Template views

# Vista para crear un usuario y renderizar el formulario
@api_view(['POST', 'GET'])
def createUserTemplate(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully")
            return redirect('get_users')
        else:
            messages.error(request, "Form data is invalid")
    else:
        form = UserForm()
    return render(request, 'crear_cliente.html', {'form': form})

@api_view(['GET', 'POST'])
def createUserAuthTemplate(request):
    if request.method == 'POST':
        formAuth = UserAuthForm(request.POST)
        if formAuth.is_valid():
            csrf_token = get_token(request)
            formCredentials = CredentialsForm(formAuth.cleaned_data)
            formCredentials.is_valid()
            apiGateway = "http://localhost:8000/auth/create/"
            response = requests.post(apiGateway, json=formCredentials.cleaned_data, headers={'X-CSRFToken': csrf_token}, cookies={'csrftoken':csrf_token})
            print(response)
            if response.status_code == 201:
                print('Entre Aquí 2')
                form = UserForm(formAuth.cleaned_data)
                form.save()
                messages.success(request, "User created successfully")
                return redirect('get_users')
        else:
            messages.error(request, "Form data is invalid")
    else:
        formAuth = UserAuthForm()
    return render(request, 'crear_cliente.html', {'form': formAuth})

# Vista para listar todos los usuarios y renderizar la lista
@api_view(['GET'])
@jwt_required
def getUsersTemplate(request):
    users = User.objects.all()
    return render(request, 'home.html', {'users': users})

# Vista para obtener detalles de un usuario específico y renderizar la información
@api_view(['GET'])
@jwt_required
def getUserTemplate(request, userId):
    try:
        user = User.objects.get(pk=userId)
        return render(request, 'cliente.html', {'user': user})
    except User.DoesNotExist:
        messages.error(request, "User not found")
        return redirect('get_users')
