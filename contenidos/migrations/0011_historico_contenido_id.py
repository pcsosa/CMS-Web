# Generated by Django 5.1 on 2024-12-05 02:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenidos', '0010_historico'),
    ]

    operations = [
        migrations.AddField(
            model_name='historico',
            name='contenido_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='contenidos.contenido'),
            preserve_default=False,
        ),
    ]
