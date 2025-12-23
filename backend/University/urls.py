from django.urls import path
from .views import (
    api_index, users_list, login, logout,
    admin_dashboard, student_dashboard, professor_dashboard,
    list_faculties, list_subjects, enroll_subject,
    admin_professors, admin_students, list_all_students,
)

urlpatterns = [
    path('', api_index),
    path('users/', users_list),
    path('login/', login),
    path('logout/', logout),
    path('faculties/', list_faculties),
    path('subjects/', list_subjects),
    path('subjects/<int:pk>/enroll/', enroll_subject),
    path('admin/', admin_dashboard),
    path('admin/professors/', admin_professors),
    path('admin/students/', admin_students),
    path('students/', list_all_students),
    path('student/', student_dashboard),
    path('professor/', professor_dashboard),
]
