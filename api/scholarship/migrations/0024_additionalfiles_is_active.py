# Generated by Django 2.2.12 on 2021-01-30 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarship', '0023_auto_20210128_0901'),
    ]

    operations = [
        migrations.AddField(
            model_name='additionalfiles',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
