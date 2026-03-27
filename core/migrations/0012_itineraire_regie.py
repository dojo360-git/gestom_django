from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0011_heuresmanuelles_presence_fk"),
    ]

    operations = [
        migrations.AddField(
            model_name="itineraire",
            name="regie",
            field=models.CharField(
                choices=[
                    ("Collecte", "Collecte"),
                    ("Precollecte", "Précollecte"),
                    ("PAV", "PAV"),
                    ("Lavage", "Lavage"),
                ],
                default="Collecte",
                max_length=20,
            ),
        ),
    ]
