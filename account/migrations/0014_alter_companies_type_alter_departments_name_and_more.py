# Generated by Django 5.0.2 on 2024-02-20 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_alter_employees_position_departments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companies',
            name='type',
            field=models.CharField(choices=[('Non IT', 'Non IT'), ('IT', 'IT')], max_length=100),
        ),
        migrations.AlterField(
            model_name='departments',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='employees',
            name='position',
            field=models.CharField(choices=[('Software Developer', 'Software Developer'), ('Project Leader', 'Project Leader'), ('Manager', 'Manager')], max_length=50),
        ),
    ]
