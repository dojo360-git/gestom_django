from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_vehicule_energie"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql=(
                        "ALTER TABLE core_presencemotif "
                        "ALTER COLUMN jour_travail TYPE boolean "
                        "USING CASE WHEN jour_travail = 0 THEN FALSE ELSE TRUE END;"
                    ),
                    reverse_sql=(
                        "ALTER TABLE core_presencemotif "
                        "ALTER COLUMN jour_travail TYPE double precision "
                        "USING CASE WHEN jour_travail THEN 1.0 ELSE 0.0 END;"
                    ),
                ),
            ],
            state_operations=[
                migrations.AlterField(
                    model_name="presencemotif",
                    name="jour_travail",
                    field=models.BooleanField(default=False),
                ),
            ],
        ),
    ]
