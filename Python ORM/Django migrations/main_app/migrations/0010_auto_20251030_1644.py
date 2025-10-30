from django.db import migrations

def set_age_group(apps, schema_editor):
    Person = apps.get_model('main_app', 'Person')
    for person in Person.objects.all():
        if person.age <= 12:
            person.age_group = 'Child'
        elif 13 <= person.age <= 17:
            person.age_group = 'Teen'
        else:  # age >= 18
            person.age_group = 'Adult'
        person.save()

class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_person'),
    ]

    operations = [
        migrations.RunPython(set_age_group),
    ]
