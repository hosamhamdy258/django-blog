# Generated by Django 4.0.6 on 2022-07-22 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0004_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='1.jpg', upload_to='imgs'),
        ),
    ]