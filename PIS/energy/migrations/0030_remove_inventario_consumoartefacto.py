# Generated by Django 4.2.7 on 2023-11-25 23:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('energy', '0029_inventario_horasdeuso'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventario',
            name='consumoArtefacto',
        ),
    ]
