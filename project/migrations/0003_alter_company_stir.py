# Generated by Django 5.1.1 on 2024-09-21 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_company_address_alter_employee_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='stir',
            field=models.CharField(max_length=64),
        ),
    ]
