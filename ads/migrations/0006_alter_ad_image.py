# Generated by Django 4.1.3 on 2022-11-02 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0005_alter_ad_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='image',
            field=models.ImageField(default='', upload_to='images/'),
        ),
    ]