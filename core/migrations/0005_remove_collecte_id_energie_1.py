from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_presencemotif_jour_travail_boolean"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="collecte",
            name="id_energie_1",
        ),
    ]
