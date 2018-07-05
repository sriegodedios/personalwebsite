# Generated by Django 2.0.6 on 2018-07-05 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_contactinformation_zip_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactinformation',
            name='address_1',
            field=models.CharField(max_length=128, verbose_name='address 1'),
        ),
        migrations.AlterField(
            model_name='contactinformation',
            name='address_2',
            field=models.CharField(blank=True, max_length=128, verbose_name='address 2'),
        ),
        migrations.AlterField(
            model_name='contactinformation',
            name='username',
            field=models.CharField(max_length=100, verbose_name='username'),
        ),
    ]
