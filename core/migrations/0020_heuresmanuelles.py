import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0019_agent_hfs_defaut"),
    ]

    operations = [
        migrations.CreateModel(
            name="HeuresManuelles",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField(default=django.utils.timezone.localdate)),
                ("heure_debut", models.TimeField(blank=True, null=True)),
                ("heure_fin", models.TimeField(blank=True, null=True)),
                ("presence", models.CharField(blank=True, max_length=150)),
                ("motif_heures_sup", models.CharField(blank=True, max_length=150)),
                ("date_creation", models.DateTimeField(auto_now_add=True)),
                ("date_modification", models.DateTimeField(auto_now=True)),
                (
                    "agent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="heures_manuelles",
                        to="core.agent",
                    ),
                ),
            ],
            options={
                "ordering": ["-date", "agent__nom", "agent__prenom", "-date_creation"],
            },
        ),
    ]
