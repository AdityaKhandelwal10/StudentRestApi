from django.db import models
from django.contrib.auth.models import AbstractUser

class Student(AbstractUser):
    email = models.EmailField()

    def __str__(self):
        return self.username