# Generated by Django 5.1.1 on 2025-04-21 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
