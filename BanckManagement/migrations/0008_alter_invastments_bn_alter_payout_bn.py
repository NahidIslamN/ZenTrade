# Generated by Django 5.0.6 on 2024-09-28 02:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BanckManagement', '0007_invastments_bn_payout_bn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invastments',
            name='BN',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='BanckManagement.bankaccount'),
        ),
        migrations.AlterField(
            model_name='payout',
            name='BN',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='BanckManagement.bankaccount'),
        ),
    ]
