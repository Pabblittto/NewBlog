# Generated by Django 2.1.7 on 2019-05-11 11:27

import Blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0006_auto_20190510_2321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profil',
            name='Zdjecie',
            field=models.ImageField(default='Profilowe/default_pic.jpg', upload_to=Blog.models.path_and_rename),
        ),
    ]
