# Generated by Django 4.1.3 on 2022-11-01 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_remove_ad_address_alter_ad_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='name',
            field=models.CharField(max_length=60),
        ),
    ]
