# Generated by Django 4.2.7 on 2024-02-19 22:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("energy", "0012_alter_perfil_imagen"),
    ]

    operations = [
        migrations.AlterField(
            model_name="perfil",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="perfil",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="perfil",
            unique_together={("user",)},
        ),
    ]