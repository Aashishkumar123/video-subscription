# Generated by Django 3.2 on 2021-07-21 07:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_lectures_course_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Accounts', '0011_auto_20210619_0940'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=300)),
                ('date', models.DateField(auto_now_add=True)),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
