# Generated by Django 3.0.8 on 2020-07-18 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0003_auto_20200718_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='account_type',
            field=models.CharField(choices=[('Savings', 'Savings'), ('Check', 'Check')], default='Savings', max_length=20),
        ),
    ]
