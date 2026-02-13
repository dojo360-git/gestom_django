from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0017_remove_agent_archive"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="agent",
            name="supp",
        ),
    ]
