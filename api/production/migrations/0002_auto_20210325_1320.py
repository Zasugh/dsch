# Generated by Django 2.2.12 on 2021-03-25 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='annualreport',
            options={'ordering': ['pk'], 'verbose_name': 'Reporte Anuales', 'verbose_name_plural': 'Listado de Reportes Anuales'},
        ),
        migrations.AlterModelOptions(
            name='typereport',
            options={'ordering': ['pk'], 'verbose_name': 'Tipo de Reporte', 'verbose_name_plural': 'Listado de Tipo de Reportes'},
        ),
    ]
