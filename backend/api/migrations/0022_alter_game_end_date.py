# Generated by Django 5.1.1 on 2025-04-21 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_game_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='end_date',
            field=models.DateField(),
        ),
    ]
