from django.db import migrations


def create_faculties(apps, schema_editor):
    Faculty = apps.get_model('University', 'Faculty')
    Faculty.objects.get_or_create(name='Computer Science')
    Faculty.objects.get_or_create(name='English')


class Migration(migrations.Migration):

    dependencies = [
        ('University', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_faculties),
    ]
