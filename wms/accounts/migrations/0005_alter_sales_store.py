# Generated by Django 3.2 on 2021-11-27 05:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_store_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.store'),
        ),
    ]
