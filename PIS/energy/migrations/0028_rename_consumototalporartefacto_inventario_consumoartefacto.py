# Generated by Django 4.2.7 on 2023-11-25 23:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('energy', '0027_inventario_nombre'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventario',
            old_name='consumoTotalPorArtefacto',
            new_name='consumoArtefacto',
        ),
    ]
