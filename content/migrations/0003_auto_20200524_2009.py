# Generated by Django 3.0.3 on 2020-05-24 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_auto_20200524_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/content/'),
        ),
    ]
