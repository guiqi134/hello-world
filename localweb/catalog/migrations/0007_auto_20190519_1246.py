# Generated by Django 2.2.1 on 2019-05-19 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_auto_20190519_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='end_time',
            field=models.TimeField(blank=True, max_length=100, null=True),
        ),
    ]