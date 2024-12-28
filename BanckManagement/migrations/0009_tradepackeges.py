# Generated by Django 5.0.6 on 2024-09-28 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BanckManagement', '0008_alter_invastments_bn_alter_payout_bn'),
    ]

    operations = [
        migrations.CreateModel(
            name='TradePackeges',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('DailyProfit', models.CharField(max_length=100)),
                ('Plan', models.CharField(max_length=100)),
                ('ReturnType', models.CharField(max_length=100)),
                ('TotalEarning', models.CharField(max_length=100)),
                ('extrachar', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
    ]
