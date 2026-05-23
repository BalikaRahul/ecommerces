from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.
class Account(AbstractBaseUser):
    first_name=models.CharField(max_length=50,blank=False)
    last_name=models.CharField(max_length=50,blank=False)
    email=models.EmailField(max_length=100,blank=False,unique=True)
    phone_number=models.CharField(max_length=50,blank=False,unique=True)

