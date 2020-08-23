# Generated by Django 3.0.8 on 2020-08-23 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='share_price_amount',
            field=models.DecimalField(decimal_places=2, default=1500, max_digits=12),
            preserve_default=False,
        ),
    ]