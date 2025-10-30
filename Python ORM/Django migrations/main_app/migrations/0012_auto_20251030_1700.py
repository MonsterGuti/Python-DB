from django.db import migrations

def set_item_rarity(apps, schema_editor):
    Item = apps.get_model('main_app', 'Item')
    for item in Item.objects.all():
        if item.price <= 10:
            item.rarity = "Rare"
        elif 11 <= item.price <= 20:
            item.rarity = "Very Rare"
        elif 21 <= item.price <= 30:
            item.rarity = "Extremely Rare"
        else:
            item.rarity = "Mega Rare"
        item.save()

class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0011_item'),
    ]

    operations = [
        migrations.RunPython(set_item_rarity),
    ]
