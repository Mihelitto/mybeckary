# Generated by Django 3.1 on 2020-11-19 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beckary_shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='img',
            field=models.ImageField(upload_to='section/'),
        ),
    ]
