# Generated by Django 3.2 on 2021-05-18 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0003_subscription_bill'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pricing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('BASIC', 'BASIC'), ('ADVANCE', 'ADVANCE'), ('VIP', 'VIP'), ('PREMIUM', 'PREMIUM')], max_length=100)),
                ('price', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=300)),
            ],
        ),
    ]
