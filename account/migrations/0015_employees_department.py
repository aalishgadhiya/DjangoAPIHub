# Generated by Django 5.0.2 on 2024-02-21 06:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_alter_companies_type_alter_departments_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employees',
            name='department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='account.departments'),
        ),
    ]
