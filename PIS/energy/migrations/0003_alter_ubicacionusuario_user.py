# Generated by Django 4.2.7 on 2024-02-10 17:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("energy", "0002_ubicacionusuario"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ubicacionusuario",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
