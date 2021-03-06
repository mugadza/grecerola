# Generated by Django 3.0.8 on 2020-07-18 13:59

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import shortuuidfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('uuid', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, unique=True, verbose_name='Public identifier')),
                ('account_name', models.CharField(blank=True, max_length=256)),
                ('account_holder_name', models.CharField(blank=True, max_length=256)),
                ('bank_name', models.CharField(blank=True, max_length=256)),
                ('account_number', models.PositiveIntegerField(unique=True, validators=[django.core.validators.MinValueValidator(100000000000), django.core.validators.MaxValueValidator(999999999999)])),
                ('account_type', models.CharField(choices=[('savings', 'savings'), ('check', 'check')], default='savings', max_length=20)),
                ('bank_branch_code', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(10000000), django.core.validators.MaxValueValidator(99999999)])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='bank', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['account_number'],
            },
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('bank', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='wallet', to='wallet.Bank')),
            ],
            options={
                'ordering': ['bank'],
                'permissions': (('can_view_wallet_report', 'Can view wallet report'),),
            },
        ),
        migrations.CreateModel(
            name='WalletLock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('wallet', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='wallet.Wallet')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('reference', models.CharField(max_length=255)),
                ('currency', models.CharField(default='ZAR', max_length=3)),
                ('transaction_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('is_pending', models.BooleanField(default=False)),
                ('confirmed_at', models.DateTimeField(blank=True, null=True)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to='wallet.Wallet')),
            ],
            options={
                'ordering': ['wallet'],
            },
        ),
    ]
