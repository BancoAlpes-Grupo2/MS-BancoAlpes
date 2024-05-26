from django.shortcuts import get_object_or_404
import jwt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User

from Auth.serializers import UserSerializer
from datetime import datetime, timedelta

from rest_framework.decorators import api_view
from django.middleware.csrf import get_token

import requests

@api_view(['POST'])
def createUser(request):
    request.data['last_name'] = request.data['role']
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get('username')
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "The username already exists."}, status=400)
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()
        payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=1),
            'username': user.username,
            'role': user.last_name
        }
        token = jwt.encode(payload, '3=tduj+4yyua6k&qx@g(xbyx69w6t_p=o$x$fcb8dw$-_g$dws', algorithm='HS256')
        response = JsonResponse({'message': "User created successfully", 'data': serializer.data}, status=201)
        response.set_cookie('authToken', token, httponly=True)
        csrf_token = get_token(request)
        apiGateway = 'http://localhost:8000/users/create/'
        requests.post(apiGateway, json=request.data, headers={'X-CSRFToken': csrf_token}, cookies={'csrftoken': csrf_token})
        return response    
    return JsonResponse(serializer.errors, status=400)

@api_view(['POST'])
def logIn(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return JsonResponse({"error": "Invalid password"}, status=400)
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=1),
        'username': user.username,
        'role': user.last_name
    }
    token = jwt.encode(payload, '3=tduj+4yyua6k&qx@g(xbyx69w6t_p=o$x$fcb8dw$-_g$dws', algorithm='HS256')
    response = HttpResponse(status=200)
    response.set_cookie('authToken', token, httponly=True)
    return response

@api_view(['GET'])
def test(request):
    response = JsonResponse({'message': "Test"}, status=200)
    response.set_cookie('authToken', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNiwiZXhwIjoxNzE2Nzg4NjAyLCJ1c2VybmFtZSI6InVzZXJnZyJ9.ChFJ1wNqkmlc44Aev2DtRhFZ9FBvf6jq4MLkSgWvjKo', httponly=True)
    return response

def generateResponse():
    response = HttpResponse('cookie')
    response.set_cookie('Test', 'test')
    return response