from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0010_collecte"),
    ]

    operations = [
        migrations.AddField(
            model_name="flux",
            name="couleur_flux",
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
