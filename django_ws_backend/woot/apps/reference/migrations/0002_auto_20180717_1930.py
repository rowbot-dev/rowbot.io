# Generated by Django 2.0.4 on 2018-07-17 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reference', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reference',
            old_name='model',
            new_name='value',
        ),
    ]
