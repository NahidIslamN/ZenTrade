# Generated by Django 5.0.6 on 2024-10-01 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BanckManagement', '0018_deposite_payadmin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deposite',
            name='Payment_Method',
        ),
    ]
