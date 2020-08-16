# Generated by Django 3.0.8 on 2020-07-23 17:40

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PayFastOrder',
            fields=[
                ('m_payment_id', models.AutoField(primary_key=True, serialize=False)),
                ('pf_payment_id', models.CharField(blank=True, max_length=40, null=True, unique=True)),
                ('payment_status', models.CharField(blank=True, max_length=20, null=True)),
                ('item_name', models.CharField(max_length=100)),
                ('item_description', models.CharField(blank=True, max_length=255, null=True)),
                ('amount_gross', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('amount_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('amount_net', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('custom_str1', models.CharField(blank=True, max_length=255, null=True)),
                ('custom_str2', models.CharField(blank=True, max_length=255, null=True)),
                ('custom_str3', models.CharField(blank=True, max_length=255, null=True)),
                ('custom_str4', models.CharField(blank=True, max_length=255, null=True)),
                ('custom_str5', models.CharField(blank=True, max_length=255, null=True)),
                ('custom_int1', models.IntegerField(blank=True, null=True)),
                ('custom_int2', models.IntegerField(blank=True, null=True)),
                ('custom_int3', models.IntegerField(blank=True, null=True)),
                ('custom_int4', models.IntegerField(blank=True, null=True)),
                ('custom_int5', models.IntegerField(blank=True, null=True)),
                ('name_first', models.CharField(blank=True, max_length=100, null=True)),
                ('name_last', models.CharField(blank=True, max_length=100, null=True)),
                ('email_address', models.CharField(blank=True, max_length=100, null=True)),
                ('merchant_id', models.CharField(max_length=15)),
                ('signature', models.CharField(blank=True, max_length=32, null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now)),
                ('request_ip', models.GenericIPAddressField(blank=True, null=True)),
                ('debug_info', models.CharField(blank=True, max_length=255, null=True)),
                ('trusted', models.NullBooleanField(default=None)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'PayFast order',
                'verbose_name_plural': 'PayFast orders',
            },
        ),
    ]
