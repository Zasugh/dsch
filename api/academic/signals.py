from django.db.models import signals, Avg
from django.dispatch import receiver

from .models import StudyPlan, Departament, AcademicStatisticsTotals, AcademicStatistics


@receiver(signal=signals.post_migrate)
def create_departament_and_plans(**kwargs):
    pass
    # study_plan_l = StudyPlan.objects.get_or_create(name='Licenciatura')
    # study_plan_m = StudyPlan.objects.get_or_create(name='Maestría')
    # study_plan_d = StudyPlan.objects.get_or_create(name='Doctorado')

    # departament_h = Departament.objects.get_or_create(name='Humanidades')
    # departament_cs = Departament.objects.get_or_create(name='Ciencias Sociales')
    # departament_ei = Departament.objects.get_or_create(name='Estudios Institucionales')


@receiver(signal=signals.post_save, sender=AcademicStatistics)
def verified_exists_average(sender, instance, **kwargs):

    if instance.totals is not None:
        totals_register = AcademicStatistics.objects.filter(totals=instance.totals)

        course_in_classroom, hour_in_classroom, student_in_classroom = 0.0, 0.0, 0.0
        course_out_classroom, hour_out_classroom, student_out_classroom = 0.0, 0.0, 0.0

        for obj in totals_register:
            if obj.classroom:

                course_in_classroom += obj.number_course
                hour_in_classroom += obj.number_hour
                student_in_classroom += obj.number_student

            else:
                course_out_classroom += obj.number_course
                hour_out_classroom += obj.number_hour
                student_out_classroom += obj.number_student

        totals = AcademicStatisticsTotals.objects.get(pk=instance.totals.pk)
        totals.course_in_classroom = course_in_classroom
        totals.hour_in_classroom = hour_in_classroom
        totals.student_in_classroom = student_in_classroom
        totals.course_out_classroom = course_out_classroom
        totals.hour_out_classroom = hour_out_classroom
        totals.student_out_classroom = student_out_classroom

        totals.save()
