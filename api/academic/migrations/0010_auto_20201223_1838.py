# Generated by Django 2.2.12 on 2020-12-24 00:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0009_auto_20201223_1809'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='academicstatistics',
            name='totals',
        ),
        migrations.DeleteModel(
            name='AcademicStatisticsTotals',
        ),
    ]
