# Generated by Django 2.1.7 on 2019-05-10 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0005_auto_20190510_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profil',
            name='Zdjecie',
            field=models.ImageField(default='default_pic.png', upload_to='Profilowe'),
        ),
    ]