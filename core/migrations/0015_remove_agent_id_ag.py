from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0014_agent_archive"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="agent",
            name="id_ag",
        ),
    ]
