from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_sample(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Faculty = apps.get_model('University', 'Faculty')
    Professor = apps.get_model('University', 'Professor')
    Student = apps.get_model('University', 'Student')
    Subject = apps.get_model('University', 'Subject')

    cs = Faculty.objects.filter(name='Computer Science').first()
    if not cs:
        cs = Faculty.objects.create(name='Computer Science')

    # create demo professor
    if not User.objects.filter(username='demo_prof').exists():
        prof_user = User.objects.create(username='demo_prof', password=make_password('pass'))
        Professor.objects.create(user=prof_user, faculty=cs, title='Dr')

    # create demo student
    if not User.objects.filter(username='demo_student').exists():
        stud_user = User.objects.create(username='demo_student', password=make_password('pass'))
        Student.objects.create(user=stud_user, faculty=cs, year=1)

    # create sample subject connecting them
    professor = Professor.objects.filter(user__username='demo_prof').first()
    student = Student.objects.filter(user__username='demo_student').first()
    if professor and student and not Subject.objects.filter(name='Intro to Programming').exists():
        subj = Subject.objects.create(name='Intro to Programming', professor=professor, faculty=cs)
        subj.students.add(student)


class Migration(migrations.Migration):

    dependencies = [
        ('University', '0002_create_faculties'),
    ]

    operations = [
        migrations.RunPython(create_sample),
    ]
