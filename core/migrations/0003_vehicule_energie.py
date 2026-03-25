from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_remove_collecte_energies_2_3"),
    ]

    operations = [
        migrations.AddField(
            model_name="vehicule",
            name="energie",
            field=models.CharField(blank=True, default="", max_length=150),
        ),
    ]
