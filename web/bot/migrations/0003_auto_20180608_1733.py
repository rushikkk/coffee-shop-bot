# Generated by Django 2.0.5 on 2018-06-08 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_auto_20180608_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coffee',
            name='cost',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='orders',
            name='cost',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='size',
            name='cost',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='syrup',
            name='cost',
            field=models.FloatField(),
        ),
    ]