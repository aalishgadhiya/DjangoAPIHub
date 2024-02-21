# Generated by Django 5.0.2 on 2024-02-21 06:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_employees_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companies',
            name='type',
            field=models.CharField(choices=[('IT', 'IT'), ('Non IT', 'Non IT')], max_length=100),
        ),
        migrations.AlterField(
            model_name='employees',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.departments'),
        ),
        migrations.AlterField(
            model_name='employees',
            name='position',
            field=models.CharField(choices=[('Manager', 'Manager'), ('Project Leader', 'Project Leader'), ('Software Developer', 'Software Developer')], max_length=50),
        ),
    ]
