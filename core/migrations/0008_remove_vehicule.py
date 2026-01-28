from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0007_rename_vehicule_date_modif"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Vehicule",
        ),
    ]
