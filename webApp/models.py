from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Costumer(models.Model):
    id = models.AutoField(primary_key=True)
    sales_person = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    email = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    info = models.CharField(max_length=256, default="")

    def __str__(self):
        return self.name


class UserChatMessage(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=256, default="")
    message_box = models.CharField(max_length=256, default="")


class PasswordsHistory(models.Model):
    user = models.CharField(max_length=256, null=True)
    pwd = models.CharField(max_length=256)
