# Generated by Django 3.1 on 2020-08-30 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='payd',
            new_name='paid',
        ),
    ]
