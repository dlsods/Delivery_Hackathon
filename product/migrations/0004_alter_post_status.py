# Generated by Django 3.2.7 on 2021-10-01 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20210929_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], max_length=10, verbose_name='Статус'),
        ),
    ]
