from django.db import models
from django.core.validators import MinValueValidator

from api.authentication.models import User
from .utils import max_value_current_year, current_year


class Departament(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['name']


class StudyPlan(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Plan de Estudio'
        verbose_name_plural = 'Planes de Estudio'
        ordering = ['name']


class Course(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos Existentes'


class AcademicStatisticsTotals(models.Model):
    course_in_classroom = models.FloatField(default=0.0)
    hour_in_classroom = models.FloatField(default=0.0)
    student_in_classroom = models.FloatField(default=0.0)
    course_out_classroom = models.FloatField(default=0.0)
    hour_out_classroom = models.FloatField(default=0.0)
    student_out_classroom = models.FloatField(default=0.0)
    year = models.PositiveIntegerField(
        default=current_year(), validators=[MinValueValidator(2000), max_value_current_year])
    created_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    study_plan = models.ForeignKey(StudyPlan, on_delete=models.CASCADE, null=True)
    departament = models.ForeignKey(Departament, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.pk } - {self.user}: {self.year} - {self.study_plan} - {self.departament}'

    class Meta:
        verbose_name = 'Estadisticas Totales de Usuario Por Año'
        verbose_name_plural = 'Estadisticas Totales Por Año'
        ordering = ['pk']


class AcademicStatistics(models.Model):

    TRIMESTER = [
        ('Invierno', 'Invierno'),
        ('Primavera', 'Primavera'),
        ('Otoño', 'Otoño'),
    ]

    number_course = models.FloatField()
    number_hour = models.FloatField()
    number_student = models.FloatField()
    classroom = models.BooleanField(default=False)
    trimester = models.CharField(max_length=15, choices=TRIMESTER, null=False)
    year = models.PositiveIntegerField(
        default=current_year(), validators=[MinValueValidator(2000), max_value_current_year])
    created_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    study_plan = models.ForeignKey(StudyPlan, on_delete=models.CASCADE, null=True)
    departament = models.ForeignKey(Departament, on_delete=models.CASCADE, null=True)
    totals = models.ForeignKey(
        AcademicStatisticsTotals, on_delete=models.CASCADE, null=True, related_name='totals')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    number_group = models.IntegerField(default=0)

    def __str__(self):
        return f'({self.pk} - {self.totals.pk}) - {self.user}: {self.trimester} - {self.year}'

    class Meta:
        verbose_name = 'Registro de Trimestre'
        verbose_name_plural = 'Registros por Trimestre'
        ordering = ['pk']
