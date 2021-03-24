from django.db import models
from django.contrib.auth.models import AbstractUser

class Student(AbstractUser):
    email = models.EmailField()

    def __str__(self):
        return self.username

class StudentVerification(models.Model):
    student_id = models.ForeignKey('Student', on_delete = models.CASCADE)
    otp = models.CharField(max_length = 12)
    created_on = models.DateTimeField(auto_now_add = True)
    modified_on = models.DateTimeField(auto_now = True)
    is_active = models.IntegerField(default = 0)