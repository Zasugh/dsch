# Generated by Django 2.2.12 on 2020-12-24 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0012_auto_20201223_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicstatisticstotals',
            name='course_in_classroom',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='academicstatisticstotals',
            name='course_out_classroom',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='academicstatisticstotals',
            name='hour_in_classroom',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='academicstatisticstotals',
            name='hour_out_classroom',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='academicstatisticstotals',
            name='student_in_classroom',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='academicstatisticstotals',
            name='student_out_classroom',
            field=models.FloatField(default=0.0),
        ),
    ]
