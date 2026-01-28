from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_energie"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Produit",
        ),
    ]
