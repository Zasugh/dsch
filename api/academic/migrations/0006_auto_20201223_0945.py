# Generated by Django 2.2.12 on 2020-12-23 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0005_auto_20201223_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departament',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='studyplan',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
