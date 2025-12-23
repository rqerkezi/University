from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Faculty, Administrator, Professor, Student, Subject


class UniversityAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # create faculties
        self.cs = Faculty.objects.create(name='Computer Science')
        self.eng = Faculty.objects.create(name='English')

    def test_register_and_dashboards(self):
        # register a professor
        resp = self.client.post('/api/register/', {'username': 'prof1', 'password': 'pass', 'role': 'professor', 'faculty_id': self.cs.id, 'title': 'Dr'})
        self.assertEqual(resp.status_code, 201)
        # register a student
        resp = self.client.post('/api/register/', {'username': 'stud1', 'password': 'pass', 'role': 'student', 'faculty_id': self.cs.id, 'year': 2})
        self.assertEqual(resp.status_code, 201)
        # obtain tokens
        resp = self.client.post('/api-token-auth/', {'username': 'prof1', 'password': 'pass'})
        self.assertEqual(resp.status_code, 200)
        token_prof = resp.data.get('token')
        resp = self.client.post('/api-token-auth/', {'username': 'stud1', 'password': 'pass'})
        token_stud = resp.data.get('token')
        # professor dashboard
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_prof)
        resp = self.client.get('/api/professor/')
        self.assertEqual(resp.status_code, 200)
        # student dashboard
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_stud)
        resp = self.client.get('/api/student/')
        self.assertEqual(resp.status_code, 200)
        # admin should be forbidden for student
        resp = self.client.get('/api/admin/')
        self.assertEqual(resp.status_code, 403)


# Create your tests here.
