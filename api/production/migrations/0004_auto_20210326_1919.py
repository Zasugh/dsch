# Generated by Django 2.2.12 on 2021-03-27 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0003_auto_20210326_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='magazinepublications',
            name='is_indexed_magazine',
            field=models.CharField(max_length=3, verbose_name='Revista Indexada'),
        ),
    ]