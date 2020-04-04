# Generated by Django 3.0.3 on 2020-04-04 17:53

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20200330_0505'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactFormMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20)),
                ('email', models.CharField(blank=True, max_length=50)),
                ('subject', models.CharField(blank=True, max_length=50)),
                ('message', models.CharField(blank=True, max_length=255)),
                ('status', models.CharField(blank=True, choices=[('Read', 'Read'), ('New', 'New')], default='New', max_length=10)),
                ('ip', models.CharField(blank=True, max_length=20)),
                ('note', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='setting',
            name='aboutus',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
        migrations.AlterField(
            model_name='setting',
            name='contact',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
        migrations.AlterField(
            model_name='setting',
            name='references',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
