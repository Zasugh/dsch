# Generated by Django 2.2.12 on 2021-01-28 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scholarship', '0022_auto_20210128_0852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionalfiles',
            name='scholarship',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='scholarship.ScholarShip'),
        ),
    ]
