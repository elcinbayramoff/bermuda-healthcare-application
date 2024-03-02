from django.db import models

# Create your models here.

class UserModel(models.Model):
    fin_code = models.CharField(unique=True,max_length=7)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    patrical_name = models.CharField(max_length=50)
    REQUIRED_FIELDS = []  # Add the required fields here
    USERNAME_FIELD = 'fin_code'
    def __str__(self):
        return f"{self.name} {self.surname}"

class AmbulanceRequest(models.Model):
    fin_code = models.CharField(max_length=7,default='1234567')
    name = models.CharField(max_length=50,default='1234567')
    surname = models.CharField(max_length=50,default='1234567')
    patrical_name = models.CharField(max_length=50,default='1234567')
    sent_time = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Ambulance Request for {self.user.name} {self.user.surname}"
