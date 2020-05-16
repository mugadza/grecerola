# Generated by Django 3.0.5 on 2020-05-14 18:59

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address_1', models.CharField(blank=True, max_length=256)),
                ('street_address_2', models.CharField(blank=True, max_length=256)),
                ('city', models.CharField(blank=True, max_length=256)),
                ('suburb', models.CharField(blank=True, max_length=128)),
                ('postal_code', models.CharField(blank=True, max_length=20)),
                ('country', django_countries.fields.CountryField(max_length=2)),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
    ]
