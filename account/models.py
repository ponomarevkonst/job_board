from django.contrib.auth.models import User
from django.db import models


class Resume(models.Model):
    user = models.ForeignKey(User, related_name="resumes", on_delete=models.CASCADE)
    phone = models.CharField(max_length=11)
    status = models.CharField(max_length=50)
    salary = models.IntegerField()
    specialty = models.CharField(max_length=50)
    grade = models.CharField(max_length=10)
    education = models.CharField(max_length=150)
    experience = models.CharField(max_length=350)
    portfolio = models.URLField()
