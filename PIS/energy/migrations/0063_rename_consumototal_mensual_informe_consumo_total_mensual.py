# Generated by Django 4.2.7 on 2023-12-15 03:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("energy", "0062_rename_consumowh_artefacto_consumo_wh_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="informe",
            old_name="consumototal_mensual",
            new_name="consumo_total_mensual",
        ),
    ]