from rest_framework import serializers
from .models import Faculty, Subject


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id', 'name']


class SubjectSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(read_only=True)
    professor = serializers.StringRelatedField()
    students = serializers.StringRelatedField(many=True)

    class Meta:
        model = Subject
        fields = ['id', 'name', 'professor', 'students', 'faculty']
