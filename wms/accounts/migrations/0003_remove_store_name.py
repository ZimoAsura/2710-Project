# Generated by Django 3.2 on 2021-11-27 05:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20211127_0542'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='name',
        ),
    ]
