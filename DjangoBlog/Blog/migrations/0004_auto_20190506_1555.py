# Generated by Django 2.1.7 on 2019-05-06 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0003_auto_20190505_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='IDBlog',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='komentarz',
            name='IDKomentarz',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='IDPost',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='profil',
            name='Zdjecie',
            field=models.ImageField(default='aaa.png', upload_to='Profilowe'),
        ),
    ]
