# Generated by Django 3.2 on 2021-05-18 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0004_pricing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pricing',
            name='id',
        ),
        migrations.AlterField(
            model_name='pricing',
            name='type',
            field=models.CharField(choices=[('BASIC', 'BASIC'), ('ADVANCE', 'ADVANCE'), ('VIP', 'VIP'), ('PREMIUM', 'PREMIUM')], max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
