from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0009_create_vehicule"),
    ]

    operations = [
        migrations.CreateModel(
            name="Collecte",
            fields=[
                ("id_collecte", models.BigAutoField(primary_key=True, serialize=False)),
                ("date_collecte", models.DateField(default=django.utils.timezone.localdate)),
                ("a1_hr_debut", models.TimeField(blank=True, null=True)),
                ("a1_hr_fin", models.TimeField(blank=True, null=True)),
                ("a2_hr_debut", models.TimeField(blank=True, null=True)),
                ("a2_hr_fin", models.TimeField(blank=True, null=True)),
                ("a3_hr_debut", models.TimeField(blank=True, null=True)),
                ("a3_hr_fin", models.TimeField(blank=True, null=True)),
                ("km_depart", models.FloatField(blank=True, null=True)),
                ("km_retour", models.FloatField(blank=True, null=True)),
                ("tonnage1", models.FloatField(blank=True, null=True)),
                ("tonnage2", models.FloatField(blank=True, null=True)),
                ("tonnage3", models.FloatField(blank=True, null=True)),
                ("energie_qte_1", models.FloatField(blank=True, null=True)),
                ("energie_qte_2", models.FloatField(blank=True, null=True)),
                ("energie_qte_3", models.FloatField(blank=True, null=True)),
                ("date_creation", models.DateTimeField(auto_now_add=True)),
                ("date_modification", models.DateTimeField(auto_now=True)),
                ("id_agent_1", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="collectes_agent_1", to="core.agent")),
                ("id_agent_2", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="collectes_agent_2", to="core.agent")),
                ("id_agent_3", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="collectes_agent_3", to="core.agent")),
                ("id_energie_1", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="collectes_energie1", to="core.energie")),
                ("id_energie_2", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="collectes_energie2", to="core.energie")),
                ("id_energie_3", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="collectes_energie3", to="core.energie")),
                ("id_flux1", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="collectes_flux1", to="core.flux")),
                ("id_flux2", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="collectes_flux2", to="core.flux")),
                ("id_flux3", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="collectes_flux3", to="core.flux")),
                ("id_vehicule", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="collectes", to="core.vehicule")),
            ],
        ),
    ]
