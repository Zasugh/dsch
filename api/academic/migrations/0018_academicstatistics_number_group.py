# Generated by Django 2.2.12 on 2021-02-11 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0017_auto_20210205_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='academicstatistics',
            name='number_group',
            field=models.IntegerField(default=0),
        ),
    ]
