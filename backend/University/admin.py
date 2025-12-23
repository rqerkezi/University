from django.contrib import admin
from .models import Administrator, Professor, Student, Subject, Faculty

admin.site.register(Administrator)
admin.site.register(Professor)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Faculty)
