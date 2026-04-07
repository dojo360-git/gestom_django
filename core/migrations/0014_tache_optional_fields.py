from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0013_tache"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tache",
            name="etat",
            field=models.CharField(
                blank=True,
                choices=[
                    ("ouvert", "ouvert"),
                    ("en_cours", "en cours"),
                    ("cloture", "clôturé"),
                ],
                default="",
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="tache",
            name="info",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
    ]
