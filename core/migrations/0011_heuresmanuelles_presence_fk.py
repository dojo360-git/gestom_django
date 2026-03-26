from django.db import migrations, models


def forwards_link_presence_motif(apps, schema_editor):
    HeuresManuelles = apps.get_model("core", "HeuresManuelles")
    PresenceMotif = apps.get_model("core", "PresenceMotif")

    pres_to_id = {}
    for motif in PresenceMotif.objects.all().only("id", "pres"):
        key = (motif.pres or "").strip()
        if key and key not in pres_to_id:
            pres_to_id[key] = motif.id

    for hm in HeuresManuelles.objects.all().only("id", "presence"):
        key = (hm.presence or "").strip()
        if not key:
            continue
        motif_id = pres_to_id.get(key)
        if motif_id:
            HeuresManuelles.objects.filter(pk=hm.pk).update(presence_motif_id=motif_id)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0010_collecte_hr_depot_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="heuresmanuelles",
            name="presence_motif",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.SET_NULL,
                related_name="heures_manuelles",
                to="core.presencemotif",
            ),
        ),
        migrations.RunPython(forwards_link_presence_motif, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="heuresmanuelles",
            name="presence",
        ),
        migrations.RenameField(
            model_name="heuresmanuelles",
            old_name="presence_motif",
            new_name="presence",
        ),
    ]
