# Generated by Django 2.2.1 on 2019-05-19 04:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20190519_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rider',
            name='AName',
            field=models.OneToOneField(limit_choices_to={'account_type': 'rider'}, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='catalog.Account'),
        ),
    ]
