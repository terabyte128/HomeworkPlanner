from django.contrib import admin

# Register your models here.
from planner.models import Course, Assignment

admin.site.register(Course)
admin.site.register(Assignment)