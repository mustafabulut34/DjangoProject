# Generated by Django 3.0.3 on 2020-05-30 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='address',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/users/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
