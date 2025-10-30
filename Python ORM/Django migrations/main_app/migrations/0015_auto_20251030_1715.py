from django.db import migrations

def set_smartphone_category(apps, schema_editor):
    Smartphone = apps.get_model('main_app', 'Smartphone')
    for phone in Smartphone.objects.all():
        if phone.price >= 750:
            phone.category = "Expensive"
        else:
            phone.category = "Cheap"
        phone.save()

class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0014_auto_20251030_1705'),
    ]

    operations = [
        migrations.RunPython(set_smartphone_category),
    ]
