from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0006_remove_produit"),
    ]

    operations = [
        migrations.RenameField(
            model_name="vehicule",
            old_name="date_modif",
            new_name="date_modification",
        ),
    ]
