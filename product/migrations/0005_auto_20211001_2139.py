# Generated by Django 3.2.7 on 2021-10-01 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_post_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='post',
            name='status',
        ),
    ]
