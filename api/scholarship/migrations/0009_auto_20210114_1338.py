# Generated by Django 2.2.12 on 2021-01-14 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarship', '0008_auto_20210114_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scholarship',
            name='file_resolution',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Archivo de Resolución'),
        ),
    ]
