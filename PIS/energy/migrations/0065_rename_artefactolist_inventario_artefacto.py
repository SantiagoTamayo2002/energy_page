# Generated by Django 4.2.7 on 2023-12-19 14:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("energy", "0064_rename_artefacto_inventario_artefactolist"),
    ]

    operations = [
        migrations.RenameField(
            model_name="inventario",
            old_name="artefactoList",
            new_name="artefacto",
        ),
    ]