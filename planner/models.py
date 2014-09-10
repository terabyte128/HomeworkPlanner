from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Course(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    period = models.IntegerField(max_length=3)
    color_code = models.CharField(max_length=6)

    def __str__(self):
        return self.user.username + ": " + self.name


class Assignment(models.Model):
    course = models.ForeignKey(Course)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    due_date = models.DateField()
    completed = models.BooleanField()
