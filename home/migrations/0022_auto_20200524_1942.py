# Generated by Django 3.0.3 on 2020-05-24 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_auto_20200524_0115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactformmessage',
            name='status',
            field=models.CharField(blank=True, choices=[('Closed', 'Closed'), ('New', 'New'), ('Read', 'Read')], default='New', max_length=10),
        ),
    ]
