# Generated by Django 3.0.3 on 2020-03-30 02:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20200330_0450'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='setting',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
