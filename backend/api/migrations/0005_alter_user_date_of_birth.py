# Generated by Django 5.1.1 on 2025-01-07 17:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_user_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(default=datetime.date(2025, 1, 7)),
            preserve_default=False,
        ),
    ]
