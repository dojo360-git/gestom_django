from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0012_itineraire_regie"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tache",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField()),
                ("info", models.CharField(max_length=255)),
                ("jour_ferie", models.BooleanField(default=False)),
                ("etat", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "taches",
                "ordering": ["date", "info"],
            },
        ),
    ]
