# Generated by Django 2.2.12 on 2020-12-23 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0004_auto_20201220_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departament',
            name='name',
            field=models.CharField(max_length=60, unique=True),
        ),
        migrations.AlterField(
            model_name='studyplan',
            name='name',
            field=models.CharField(max_length=60, unique=True),
        ),
    ]
