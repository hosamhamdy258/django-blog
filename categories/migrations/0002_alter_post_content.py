# Generated by Django 4.0.6 on 2022-07-21 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(help_text='Max length is 4000', max_length=4000),
        ),
    ]