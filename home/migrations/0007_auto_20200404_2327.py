# Generated by Django 3.0.3 on 2020-04-04 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20200404_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactformmessage',
            name='status',
            field=models.CharField(blank=True, choices=[('Read', 'Read'), ('New', 'New')], default='New', max_length=10),
        ),
    ]
