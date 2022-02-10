# Generated by Django 3.2 on 2021-05-21 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0006_pricing_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricing',
            name='duration',
            field=models.CharField(choices=[('month', 'mo'), ('year', 'yr')], max_length=50),
        ),
        migrations.AlterField(
            model_name='subscription_bill',
            name='subscription_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accounts.pricing'),
        ),
    ]