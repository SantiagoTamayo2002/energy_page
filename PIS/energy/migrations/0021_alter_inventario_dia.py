# Generated by Django 4.2.7 on 2023-11-23 21:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('energy', '0020_remove_inventario_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventario',
            name='dia',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
