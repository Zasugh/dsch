# Generated by Django 2.2.12 on 2021-01-28 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scholarship', '0021_auto_20210127_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholarship',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='AdditionalFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_file', models.CharField(max_length=10)),
                ('file', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('scholarship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scholarship.ScholarShip')),
            ],
            options={
                'verbose_name': 'Archivo Adicional',
                'verbose_name_plural': 'Documentación Relacionada',
                'ordering': ['pk'],
            },
        ),
    ]