# Generated by Django 2.2.12 on 2021-01-17 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarship', '0015_auto_20210117_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scholarship',
            name='date_get_request',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fecha de respuesta'),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='date_request',
            field=models.DateTimeField(verbose_name='Fecha de Solicitud'),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='date_send_request',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fecha de envío a la dictaminadora'),
        ),
    ]
