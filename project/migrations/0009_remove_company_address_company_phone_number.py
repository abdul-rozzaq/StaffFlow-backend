# Generated by Django 5.1.3 on 2025-01-11 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_employee_passport'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='address',
        ),
        migrations.AddField(
            model_name='company',
            name='phone_number',
            field=models.CharField(blank=True, default=None, max_length=13, null=True),
        ),
    ]
