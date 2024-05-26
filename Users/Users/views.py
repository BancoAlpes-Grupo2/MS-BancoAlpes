from django.http import JsonResponse
from rest_framework.decorators import api_view

from Users.forms import userForm
from Users.models import User
from Users.utils.authentication import jwt_required

@api_view(['POST'])
def createUser(request):
    form = userForm(request.data)
    if form.is_valid():
        form.save()
        return JsonResponse({"message": "User created successfully"}, status=201)
    return JsonResponse({"error": "Form data is invalid", "details": form.errors}, status=400)

@api_view(['GET'])
@jwt_required
def getUsers(request):
    users = User.objects.all()
    users = [{"name": user.name, "lastName": user.lastName, "country": user.country, "city": user.city, "phone": user.phone, "email": user.email} for user in users]
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
        #print(request.user_id)
        return JsonResponse(userData, status=200)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
