# Generated by Django 3.0.3 on 2020-05-22 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_auto_20200523_0142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactformmessage',
            name='status',
            field=models.CharField(blank=True, choices=[('Read', 'Read'), ('New', 'New'), ('Closed', 'Closed')], default='New', max_length=10),
        ),
    ]
