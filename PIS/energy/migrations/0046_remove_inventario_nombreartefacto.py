# Generated by Django 4.2.7 on 2023-12-13 18:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("energy", "0045_alter_informe_user_alter_inventario_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="inventario",
            name="nombreArtefacto",
        ),
    ]