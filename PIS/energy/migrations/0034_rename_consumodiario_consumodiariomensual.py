# Generated by Django 4.2.7 on 2023-11-26 04:04

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('energy', '0033_rename_consumosdiarios_consumodiario'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='consumoDiario',
            new_name='ConsumoDiarioMensual',
        ),
    ]
