# Generated by Django 3.2 on 2021-04-16 03:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_newuser_last_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newuser',
            options={'verbose_name_plural': 'Users'},
        ),
    ]