# Generated by Django 3.2 on 2021-11-30 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_sales_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales',
            name='email',
            field=models.EmailField(max_length=200, null=True),
        ),
    ]
