from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Course(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, null=True)
    period = models.IntegerField(max_length=3, null=True)

    def __str__(self):
        return self.user.username + ": " + self.name


class Assignment(models.Model):
    course = models.ForeignKey(Course)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, null=True)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.course.user.username + ": " + self.name