# Generated by Django 2.2.12 on 2021-01-19 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarship', '0016_auto_20210117_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholarship',
            name='number_receipt_dictum',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Folio de dictamen'),
        ),
    ]
