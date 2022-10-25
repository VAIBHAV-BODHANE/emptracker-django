# Generated by Django 4.1.2 on 2022-10-20 22:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpDetails', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employees',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='employees',
            name='designation',
            field=models.CharField(default='a', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employees',
            name='jod',
            field=models.DateField(default=datetime.date(2022, 10, 21)),
        ),
    ]
