# Generated by Django 4.2.7 on 2023-12-19 14:36

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("energy", "0063_rename_consumototal_mensual_informe_consumo_total_mensual"),
    ]

    operations = [
        migrations.RenameField(
            model_name="inventario",
            old_name="artefacto",
            new_name="artefactoList",
        ),
    ]