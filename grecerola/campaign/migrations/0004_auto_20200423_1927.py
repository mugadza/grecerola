# Generated by Django 3.0.5 on 2020-04-23 19:27

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0003_auto_20200423_1906'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaignimage',
            name='height',
        ),
        migrations.RemoveField(
            model_name='campaignimage',
            name='ppoi',
        ),
        migrations.RemoveField(
            model_name='campaignimage',
            name='width',
        ),
        migrations.AlterField(
            model_name='campaignimage',
            name='image',
            field=versatileimagefield.fields.VersatileImageField(default='placeholder1080x1080.png', upload_to='campaigns', verbose_name='image'),
        ),
    ]
