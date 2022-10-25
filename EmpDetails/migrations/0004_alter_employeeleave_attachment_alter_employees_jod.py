# Generated by Django 4.1.2 on 2022-10-22 09:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('EmpDetails', '0003_alter_employees_designation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeleave',
            name='attachment',
            field=models.ImageField(blank=True, null=True, upload_to='employee/attachment/images'),
        ),
        migrations.AlterField(
            model_name='employees',
            name='jod',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
