# Generated by Django 5.0.6 on 2024-09-25 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthApp', '0003_customuser_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='state',
            field=models.TextField(blank=True, null=True),
        ),
    ]
