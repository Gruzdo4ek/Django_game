# Generated by Django 5.1.1 on 2024-09-10 04:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0005_platform'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='platform_fk',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='games.platform'),
        ),
    ]
