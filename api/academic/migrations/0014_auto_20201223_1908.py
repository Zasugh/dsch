# Generated by Django 2.2.12 on 2020-12-24 01:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0013_auto_20201223_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicstatistics',
            name='totals',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='totals', to='academic.AcademicStatisticsTotals'),
        ),
    ]
