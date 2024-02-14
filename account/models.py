from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None,password2=None,gender=None):
       if not email:
           raise ValueError("Users must have an email address")
       user = self.model(
           email=self.normalize_email(email),
           username=username,
           first_name=first_name,
           last_name=last_name,
           gender=gender,
           
       )
       user.set_password(password)
       user.save(using=self._db)
       return user
   
   
    def create_superuser(self, email, username, first_name, last_name, password=None, gender=None):
        user = self.create_user(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            gender=gender,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    

# Create your models here.

class Users(AbstractBaseUser):
    username = models.CharField(max_length=150,unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(verbose_name='Email',max_length=255,unique=True)
    gender_choices=[
        ('M','Male'),
        ('F','Female')
    ]
    gender = models.CharField(max_length=1,choices=gender_choices)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name','gender']
    
    
    def __str__(self):
        return self.email
    
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    
    
