from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0018_remove_agent_supp"),
    ]

    operations = [
        migrations.AddField(
            model_name="agent",
            name="hfs_defaut",
            field=models.TimeField(blank=True, null=True),
        ),
    ]
