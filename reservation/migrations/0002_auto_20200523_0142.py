# Generated by Django 3.0.3 on 2020-05-22 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='admin_note',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='reservation',
            name='days',
            field=models.IntegerField(blank=True, default=1),
        ),
        migrations.AddField(
            model_name='reservation',
            name='phone',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
