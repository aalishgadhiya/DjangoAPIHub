# Generated by Django 5.0.2 on 2024-02-20 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_alter_employees_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='position',
            field=models.CharField(choices=[('Manager', 'Manager'), ('Software Developer', 'Software Developer'), ('Project Leader', 'Project Leader')], max_length=50),
        ),
    ]