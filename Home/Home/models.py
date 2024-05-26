from django.db import models

class User(models.Model):
    name = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=50)

class Credentials(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)