# Generated by Django 3.2 on 2021-06-18 14:28

from django.db import migrations, models
import django_countries.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0009_alter_profile_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='unique_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=django_countries.fields.CountryField(max_length=255),
        ),
    ]