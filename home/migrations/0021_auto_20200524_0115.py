# Generated by Django 3.0.3 on 2020-05-23 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_auto_20200523_0232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactformmessage',
            name='status',
            field=models.CharField(blank=True, choices=[('Closed', 'Closed'), ('Read', 'Read'), ('New', 'New')], default='New', max_length=10),
        ),
    ]
