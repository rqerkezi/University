from django.contrib.auth.models import User
from django.db import models

class Faculty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    class Meta:
        abstract = True
class Administrator(Person):
    def __str__(self):
        return self.user.username

class Professor(Person):
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} ({self.title})"

class Student(Person):
    year = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} (Year {self.year})"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
