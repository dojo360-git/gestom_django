from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0016_remove_agent_hajout_quotidien"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="agent",
            name="archive",
        ),
    ]
