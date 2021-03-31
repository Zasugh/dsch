# Generated by Django 2.2.12 on 2021-01-28 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarship', '0020_scholarship_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholarship',
            name='result_permanence',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='scholarship',
            name='result_promotion',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='scholarship',
            name='result_stimulus',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='scholarship',
            name='result_trajectory',
            field=models.IntegerField(default=0),
        ),
    ]