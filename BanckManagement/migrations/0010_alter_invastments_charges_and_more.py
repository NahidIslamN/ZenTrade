# Generated by Django 5.0.6 on 2024-09-29 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BanckManagement', '0009_tradepackeges'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invastments',
            name='Charges',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='invastments',
            name='Txn_Details',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]