from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0015_remove_agent_id_ag"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="agent",
            name="hajout_quotidien",
        ),
    ]
