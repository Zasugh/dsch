from django.db import models

from api.authentication.models import User


class OptionRequest(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Opción de Solicitud'
        verbose_name_plural = 'Opciones para Solicitud de Becas'
        ordering = ['pk']


class ScholarShip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_request = models.DateTimeField(verbose_name='Fecha de Solicitud')
    number_request = models.CharField(
        verbose_name='Número de Solicitud', max_length=15, null=False, blank=False)
    file_request = models.CharField(verbose_name='Archivo de Solicitud', max_length=100)
    date_send_request = models.DateTimeField(
        verbose_name='Fecha de envío a la dictaminadora', null=True, blank=True)

    date_get_request = models.DateTimeField(
        verbose_name='Fecha de respuesta', null=True, blank=True)
    number_dictum = models.CharField(
        verbose_name='Folio de dictamen', max_length=20, null=True, blank=True)
    file_dictum = models.CharField(
        verbose_name='Archivo de Acuse de Dictamen', max_length=100, null=True, blank=True)
    number_receipt_dictum = models.CharField(
        verbose_name='Folio de Acuse de Dictamen', max_length=20, null=True, blank=True)
    file_receipt_dictum = models.CharField(
        verbose_name='Archivo de Acuse', max_length=100, null=True, blank=True)

    number_notification = models.CharField(
        verbose_name='Folio de Notificación de Recepción',
        max_length=20, null=True, blank=True)
    file_notification= models.CharField(
        verbose_name='Archivo de Notificación de Recepción',
        max_length=100, null=True, blank=True)

    number_resolution = models.CharField(
        verbose_name='Folio de Resolución', max_length=20, null=True, blank=True)
    file_resolution = models.CharField(
        verbose_name='Archivo de Resolución', max_length=100, null=True, blank=True)

    number_reply = models.CharField(
        verbose_name='Folio de Respuesta de Comisión Dictaminadora', max_length=20,
        null=True, blank=True)
    file_reply = models.CharField(
        verbose_name='Archivo de Respuesta de Comisión Dictaminadora', max_length=100,
        null=True, blank=True)

    number_bis = models.CharField(
        verbose_name='Folio de Dictamen BIS', max_length=20, null=True, blank=True)
    file_bis = models.CharField(
        verbose_name='Archivo de Dictamen BIS', max_length=100, null=True, blank=True)

    number_receipt_bis = models.CharField(
        verbose_name='Folio de Acuse de Recibido de Dictamen', max_length=20,
        null=True, blank=True)
    file_receipt_bis = models.CharField(
        verbose_name='Archivo de Acuse de Recibido de Dictament', max_length=100,
        null=True, blank=True)

    year = models.IntegerField(null=False, blank=False, default=2020)
    finalized = models.BooleanField(default=False)

    promotion = models.BooleanField(default=False)
    stimulus = models.BooleanField(default=False)
    trajectory = models.BooleanField(default=False)
    permanence = models.BooleanField(default=False)

    years = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    result_promotion = models.IntegerField(default=0)
    result_stimulus = models.IntegerField(default=0)
    result_trajectory = models.IntegerField(default=0)
    result_permanence = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        request = ''

        if self.permanence:
            request = 'BECA DE APOYO A LA PERMANENCIA '+str(self.years)+'  ||  '

        if self.promotion:
            request += 'PROMOCIÓN'+'  ||  '

        if self.trajectory:
            request += 'ESTÍMULO A LA TRAYECTORIA ACADÉMICA SOBRESALIENTE'+'  ||  '

        if self.stimulus:
            request += 'ESTÍMULO A LA DOCENCIA E INVESTIGACIÓN'+'  ||  '

        return f'({self.pk} - {self.is_active}) {self.user}: {self.number_request} - {request}'

    class Meta:
        verbose_name = 'Solicitud de Beca'
        verbose_name_plural = 'Solicitudes de Beca'
        ordering = ['date_request']


class AdditionalFiles(models.Model):
    scholarship = models.ForeignKey(ScholarShip, related_name='files', on_delete=models.CASCADE)
    number_file = models.CharField(max_length=10, null=False, blank=False)
    file = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.scholarship}: {self.number_file} - {self.file}'

    class Meta:
        verbose_name = 'Archivo Adicional'
        verbose_name_plural = 'Documentación Relacionada'
        ordering = ['pk']
