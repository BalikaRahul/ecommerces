from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.
# this is for creating normal user
class MyAccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,phone_number,password=None):
        if not email:
            raise ValueError('user must has an email address')
        if not username:
            raise ValueError('user must have an username')
        user = self.model(
            email =self.normalize_email(email), #normalize_email is used in case if the user enter the email in upper case it will convert it into small case
            username =username,
            first_name= first_name,
            last_name = last_name,
            phone_number=phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
# this is for creating super user
    def create_superuser(self,first_name,last_name,email,username,phone_number,password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password =password,
            first_name = first_name,
            last_name=last_name,
            phone_number=phone_number,
        )
# permission for the superuser
        user.is_admin =True
        user.is_active = True
        user.is_staff =True
        user.is_superadmin = True
        user.save(using = self._db)
        return user


# this is Account  
class Account(AbstractBaseUser):
    first_name=models.CharField(max_length=50,blank=False)
    last_name=models.CharField(max_length=50,blank=False)
    username = models.CharField(max_length=50, unique=True)
    email=models.EmailField(max_length=100,blank=False,unique=True)
    phone_number=models.CharField(max_length=50,blank=False,unique=True)

    #required fiels
    date_joined =models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name','phone_number']
    objects = MyAccountManager()
    
    # shows the email 
    def __str__(self):
        return self.email
    
    # if the user is admin he has all the permission to change the thing 
    def has_perm(self,perm,obj=None):# perm should singular
        return self.is_admin
    # permission
    def has_module_perms(self,app_label):
        return True