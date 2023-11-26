# Generated by Django 4.2.7 on 2023-11-23 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('energy', '0016_inventario_user_alter_inventario_dia'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventario',
            name='consumoTotal',
        ),
        migrations.RemoveField(
            model_name='inventario',
            name='consumoTotalPorArtefacto',
        ),
        migrations.RemoveField(
            model_name='inventario',
            name='dia',
        ),
        migrations.RemoveField(
            model_name='inventario',
            name='nombre',
        ),
        migrations.RemoveField(
            model_name='inventario',
            name='artefacto',
        ),
        migrations.AddField(
            model_name='inventario',
            name='artefacto',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='artefactoList', to='energy.artefactos'),
            preserve_default=False,
        ),
    ]
