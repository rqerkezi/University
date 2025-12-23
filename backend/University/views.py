from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework.exceptions import NotFound
from .models import Administrator, Professor, Student, Subject, Faculty
from .serializers import FacultySerializer, SubjectSerializer

# Registration endpoint
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a user and create the related Person subclass.
    Expected payload: { username, password, role, faculty_id, title (for professor), year (for student) }
    """
    data = request.data
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    faculty_id = data.get('faculty_id')

    if not username or not password or not role:
        return Response({'detail': 'username, password and role are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'detail': 'username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        faculty = Faculty.objects.get(id=faculty_id)
    except Exception:
        return Response({'detail': 'invalid faculty_id.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)

    role = role.lower()
    if role == 'administrator':
        Administrator.objects.create(user=user, faculty=faculty)
    elif role == 'professor':
        title = data.get('title', '')
        Professor.objects.create(user=user, faculty=faculty, title=title)
    elif role == 'student':
        year = data.get('year')
        try:
            year = int(year)
        except Exception:
            return Response({'detail': 'student role requires integer year field.'}, status=status.HTTP_400_BAD_REQUEST)
        Student.objects.create(user=user, faculty=faculty, year=year)
    else:
        user.delete()
        return Response({'detail': 'invalid role'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'detail': 'user registered'}, status=status.HTTP_201_CREATED)


# Role-aware dashboards
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_dashboard(request):
    if not Administrator.objects.filter(user=request.user).exists():
        return Response({'detail': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)
    return Response({"role": "Administrator Dashboard"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_dashboard(request):
    if not Student.objects.filter(user=request.user).exists():
        return Response({'detail': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)
    student = Student.objects.get(user=request.user)
    # return subjects the student is enrolled in
    subjects = Subject.objects.filter(students=student)
    serializer = SubjectSerializer(subjects, many=True)
    return Response({"role": "Student Dashboard", "subjects": serializer.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def professor_dashboard(request):
    if not Professor.objects.filter(user=request.user).exists():
        return Response({'detail': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)
    professor = Professor.objects.get(user=request.user)
    subjects = Subject.objects.filter(professor=professor)
    serializer = SubjectSerializer(subjects, many=True)
    return Response({"role": "Professor Dashboard", "subjects": serializer.data})


# List faculties and subjects
@api_view(['GET'])
@permission_classes([AllowAny])
def list_faculties(request):
    faculties = Faculty.objects.all()
    serializer = FacultySerializer(faculties, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_subjects(request):
    subjects = Subject.objects.all()
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def users_list(request):
    """Return all users (id and username)."""
    users = list(User.objects.all().values('id', 'username'))
    return Response(users)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_faculties(request):
    faculties = Faculty.objects.all()
    serializer = FacultySerializer(faculties, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_subjects(request):
    subjects = Subject.objects.all()
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enroll_subject(request, pk):
    """Enroll the authenticated student into a subject."""
    # ensure user is a student
    if not Student.objects.filter(user=request.user).exists():
        return Response({'detail': 'only students can enroll'}, status=status.HTTP_403_FORBIDDEN)
    student = Student.objects.get(user=request.user)
    try:
        subject = Subject.objects.get(id=pk)
    except Subject.DoesNotExist:
        return Response({'detail': 'subject not found'}, status=status.HTTP_404_NOT_FOUND)
    subject.students.add(student)
    subject.save()
    serializer = SubjectSerializer(subject)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_professors(request):
    if not Administrator.objects.filter(user=request.user).exists():
        return Response({'detail': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)
    profs = Professor.objects.all()
    data = [{'id': p.user.id, 'username': p.user.username, 'title': p.title, 'faculty': p.faculty.name} for p in profs]
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_students(request):
    if not Administrator.objects.filter(user=request.user).exists():
        return Response({'detail': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)
    studs = Student.objects.all()
    data = [{'id': s.user.id, 'username': s.user.username, 'year': s.year, 'faculty': s.faculty.name} for s in studs]
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_all_students(request):
    """Return all students (id, username, year, faculty) for authenticated users."""
    studs = Student.objects.all()
    data = [{'id': s.user.id, 'username': s.user.username, 'year': s.year, 'faculty': s.faculty.name} for s in studs]
    return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Authenticate user and return token."""
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'detail': 'username and password required'}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'detail': 'invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    token, _ = Token.objects.get_or_create(user=user)
    # determine role
    role = None
    if Administrator.objects.filter(user=user).exists():
        role = 'administrator'
    elif Professor.objects.filter(user=user).exists():
        role = 'professor'
    elif Student.objects.filter(user=user).exists():
        role = 'student'
    return Response({'token': token.key, 'id': user.id, 'username': user.username, 'role': role})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Log out by deleting the current user's token."""
    Token.objects.filter(user=request.user).delete()
    return Response({'detail': 'logged out'})


@api_view(['GET'])
@permission_classes([AllowAny])
def api_index(request):
    """Return a small JSON index of available API endpoints (visible only in DEBUG)."""
    if not settings.DEBUG:
        raise NotFound()
    return Response({
        'message': 'University API',
        'endpoints': {
            'users': '/api/users/',
            'login': '/api/login/',
            'logout': '/api/logout/',
            'faculties': '/api/faculties/',
            'subjects': '/api/subjects/',
            'subject_enroll': '/api/subjects/{id}/enroll/',
            'admin_dashboard': '/api/admin/',
            'admin_professors': '/api/admin/professors/',
            'admin_students': '/api/admin/students/',
            'student_dashboard': '/api/student/',
            'professor_dashboard': '/api/professor/',
        }
    })
