from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0008_remove_vehicule"),
    ]

    operations = [
        migrations.CreateModel(
            name="Vehicule",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nom_vehicule", models.CharField(max_length=150)),
                ("type", models.CharField(max_length=150)),
                ("archive", models.BooleanField(default=False)),
                ("date_creation", models.DateTimeField(auto_now_add=True)),
                ("date_modification", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
