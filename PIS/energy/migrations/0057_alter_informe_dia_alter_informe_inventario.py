# Generated by Django 4.2.7 on 2023-12-14 01:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("energy", "0056_alter_informe_inventario"),
    ]

    operations = [
        migrations.AlterField(
            model_name="informe",
            name="dia",
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="informe",
            name="inventario",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="inventario",
                to="energy.inventario",
            ),
        ),
    ]