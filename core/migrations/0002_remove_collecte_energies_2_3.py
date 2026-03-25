from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="collecte",
            name="id_energie_2",
        ),
        migrations.RemoveField(
            model_name="collecte",
            name="id_energie_3",
        ),
        migrations.RemoveField(
            model_name="collecte",
            name="energie_qte_2",
        ),
        migrations.RemoveField(
            model_name="collecte",
            name="energie_qte_3",
        ),
    ]
