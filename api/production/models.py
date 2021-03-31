from django.db import models

from api.authentication.models import User
from api.academic.models import Departament


class AnnualReport(models.Model):
    # Reporte Anual
    date_created = models.DateTimeField(auto_now_add=True)
    year = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f'{self.pk}: {self.year}'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Reporte Anuales'
        verbose_name_plural = 'Listado de Reportes Anuales'


class TypeReport(models.Model):
    # Tipo de Reporte
    name = models.CharField(
        verbose_name='Nombre de Reporte', null=False, blank=False, max_length=100)

    def __str__(self):
        return f'{self.pk}: {self.name}'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Tipo de Reporte'
        verbose_name_plural = 'Listado de Tipo de Reportes'


class GeneralFieldsOfModels(models.Model):
    annual_report = models.ForeignKey(
        AnnualReport, on_delete=models.CASCADE, null=False, related_name='%(class)s')
    type_report = models.ForeignKey(
        TypeReport, on_delete=models.CASCADE, null=False, related_name='%(class)s')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, related_name='%(class)s')

    class Meta:
        abstract = True


class TeacherTraining(GeneralFieldsOfModels):
    # Actualización y Formación Docente
    name = models.CharField(
        verbose_name='Nombre de Actividad', null=False, blank=False, max_length=250)
    institute = models.CharField(
        verbose_name='Instituto', null=False, blank=False, max_length=250)
    type_activity = models.CharField(
        verbose_name='Tipo de Actividad', null=False, blank=False, max_length=50)
    hours = models.IntegerField(verbose_name='Número de Horas', null=False, blank=False)

    def __str__(self):
        return f'({self.pk}) - {self.user.number}: {self.type_activity} - {self.name}'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Formación Docente'
        verbose_name_plural = 'Listado de Formación Docente'


class ExchangeActivity(GeneralFieldsOfModels):
    # Actividad de Intercambio
    division = models.CharField(
        verbose_name='División', null=False, blank=False, max_length=10)
    activity = models.CharField(
        'Actividad de Intercambio', null=False, blank=False, max_length=50)
    ies = models.CharField(
        verbose_name='Nombre de la IES', null=False, blank=False, max_length=250)
    country = models.CharField('Cuidad, País de IES', null=False, blank=False, max_length=150)

    def __str__(self):
        return f'{self.pk}: {self.user.number} - ({self.ies}: {self.country})'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Actividad de Intercambio'
        verbose_name_plural = 'Listado de Actividad de Intercambio'


class AcademicEvents(GeneralFieldsOfModels):
    # Eventos Acádemicos
    name = models.TextField(verbose_name='Nombre de Evento', null=False, blank=False)
    institute = models.CharField(verbose_name='Institución Sede', null=True, max_length=250)
    country = models.CharField(verbose_name='Cuidad/Paía', null=True, max_length=100)
    range_date = models.CharField(verbose_name='Rango de Fechas', null=True, max_length=100)
    type_activity = models.CharField(
        verbose_name='Tipo de Actividad', null=False, blank=False, max_length=255)

    def __str__(self):
        return f'{self.pk}: {self.name} -({self.institute}, {self.country}: {self.range_date})'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Evento Acádemico'
        verbose_name_plural = 'Listado de Eventos Acádemicos'


class AcademicCollaboration(GeneralFieldsOfModels):
    # Redes de Colaboración Acádemica
    name = models.CharField(
        verbose_name='Nombre de Red Acádemica', null=False, blank=False, max_length=200)
    institutions = models.TextField(
        verbose_name='Instituciones Pertenecientes a la Red', null=False, blank=False)
    activities = models.TextField(verbose_name='Actividades Destacadas', null=True)

    def __str__(self):
        return f'{self.pk}: {self.name} -> {self.institutions}'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Red de Colaboración'
        verbose_name_plural = 'Listado de Redes de Colaboración Acádemica'


class ProjectCollaboration(GeneralFieldsOfModels):
    # Colaboración de Proyectos
    name = models.TextField(verbose_name='Nombre de Proyecto', null=False, blank=False)
    organizations = models.CharField(
        verbose_name='Organizaciones Participantes', null=True, max_length=255)
    sector = models.CharField(verbose_name='Sector', null=True, max_length=20)

    def __str__(self):
        return f'{self.pk}: {self.user.number} ({self.sector} -> {self.organizations})'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Listado de Colaboraciones en Proyectos'


class MagazinePublications(GeneralFieldsOfModels):
    # Publicación en Revistas
    user = models.ManyToManyField(User, related_name='%(class)s')
    title = models.TextField(verbose_name='Título de Arículo', null=False, blank=False)
    magazine_name = models.CharField(verbose_name='Nombre de Revista', null=True, max_length=200)
    number = models.IntegerField(verbose_name='Número', null=True)
    volume = models.CharField(verbose_name='Volumen', null=True, max_length=50)
    pages = models.CharField(verbose_name='Páginas', null=True, max_length=50)
    is_indexed_magazine = models.CharField(
        verbose_name='Revista Indexada', max_length=3, null=False, blank=False)
    type_job = models.CharField(
        verbose_name='Tipo de Trabajo', null=False, blank=False, max_length=200)

    def __str__(self):
        return f'{self.pk}: {self.title} ({self.magazine_name} -> {self.is_indexed_magazine})'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Publicación en Revista'
        verbose_name_plural = 'Listado de Publicaciones en Revistas'


class ElectronicJournals(GeneralFieldsOfModels):
    # Revistas Electrónicas
    user = models.ManyToManyField(User, related_name='%(class)s')
    title = models.CharField(
        verbose_name='Título de Articulo', null=False, blank=False, max_length=255)
    magazine_name = models.CharField(
        verbose_name='Nombre de Revista Electrónica', null=True, max_length=200)
    number = models.CharField(verbose_name='Número', null=True, max_length=100)
    volume = models.CharField(verbose_name='Volumen', null=True, max_length=15)
    pages = models.CharField(verbose_name='Páginas', null=True, max_length=15)
    doi = models.URLField(verbose_name='DOI o Ubicacion de Internet', null=True)
    type_job = models.CharField(
        verbose_name='Tipo de Trabajo', null=False, blank=False, max_length=100)

    def __str__(self):
        return f'{self.pk}: {self.title} ({self.magazine_name} -> {self.doi})'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Revista Electrónica'
        verbose_name_plural = 'Listado de Revistas Electrónicas'


class NewspaperPublication(GeneralFieldsOfModels):
    # Publicaciones en Periódicos
    user = models.ManyToManyField(User, related_name='%(class)s')
    date = models.DateTimeField()
    title = models.CharField(
        verbose_name='Título de Artículo', null=False, blank=False, max_length=255)
    newspaper_name = models.CharField(
        verbose_name='Nombre de periódico', null=False, blank=False, max_length=100)
    section = models.CharField(verbose_name='Sección (Letra)', null=True, max_length=50)
    pages = models.CharField(verbose_name='Páginas', null=True, max_length=15)
    type_job = models.CharField(verbose_name='Tipo de Trabajo', null=True, max_length=15)

    def __str__(self):
        return f'{self.pk}: {self.title} ({self.newspaper_name} -> {self.type_job})'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Pulicación en Periódico'
        verbose_name_plural = 'Listado de Publicaciones en Periódicos'


class PublishedBooks(GeneralFieldsOfModels):
    # Libros Publicados
    user = models.ManyToManyField(User, related_name='%(class)s')
    title = models.CharField(
        verbose_name='Título de Libro', null=False, blank=False, max_length=255)
    edition = models.CharField(verbose_name='Edición', null=True, max_length=100)
    place = models.CharField(verbose_name='Lugar', null=False, blank=False, max_length=60)
    editorial = models.CharField(
        verbose_name='Editorial', null=False, blank=False, max_length=100)
    isbn = models.CharField(verbose_name='ISBN', null=True, max_length=30)
    type_job = models.CharField(
        verbose_name='Tipo de Investigación', null=True, max_length=30)

    def __str__(self):
        return f'{self.pk}: {self.title} ({self.editorial} -> {self.place})'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Libro Publicado'
        verbose_name_plural = 'Listado de Libros Publicados'


class ChaptersBooks(GeneralFieldsOfModels):
    # Capítulos de Libros
    departament = models.ForeignKey(Departament, on_delete=models.CASCADE)
    user = models.ManyToManyField(User, related_name='%(class)s')
    name = models.CharField(
        verbose_name='Nombre de Capítulo', null=False, blank=False, max_length=255)
    bibliographic_file = models.TextField(
        verbose_name='Ficha Bibliográfica de Libro', null=True)

    def __str__(self):
        return f'{self.pk}: {self.name} ({self.departament} -> {self.bibliographic_file[:30]})'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Capítulo de Libro'
        verbose_name_plural = 'Listado de Capítulos de Libros'


class BookReviews(GeneralFieldsOfModels):
    # Reseñas de Libros
    title = models.CharField(
        verbose_name='Título de Reseña', null=False, blank=False, max_length=255)
    book = models.CharField(
        verbose_name='Título de Libro', null=False, blank=False, max_length=200)
    publication = models.CharField(
        verbose_name='Título de Publicación', null=False, blank=False, max_length=200)
    number = models.CharField(verbose_name='Número', null=True, max_length=100)
    volume = models.CharField(verbose_name='Volumen', null=True, max_length=15)
    pages = models.CharField(verbose_name='Páginas', null=True, max_length=15)

    def __str__(self):
        return f'{self.pk}: {self.title} ({self.book[:30]} -> {self.publication})'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Reseña de Libro'
        verbose_name_plural = 'Listado de Reseñas de Libros'


class PublishedLectures(GeneralFieldsOfModels):
    # Conferencias Publicadas
    user = models.ManyToManyField(User, related_name='%(class)s')
    title = models.CharField(
        verbose_name='Título de Conferencia', null=False, blank=False, max_length=200)
    editor = models.CharField(
        verbose_name='Nombre de Editor', null=True, blank=True, max_length=200)
    ed = models.CharField(verbose_name='Editorial (s)', null=True, max_length=200)
    congress = models.CharField(
        verbose_name='Título de Congreso', null=False, blank=False, max_length=200)
    pages = models.CharField(verbose_name='Páginas', null=True, max_length=15)
    place = models.CharField(verbose_name='Lugar', null=False, blank=False, max_length=50)
    editorial = models.CharField(verbose_name='Editorial', null=True, max_length=100)
    type_job = models.CharField(verbose_name='Tipo de Investigación', null=True, max_length=30)

    def __str__(self):
        return f'{self.pk}: {self.title[:70]} ({self.congress} -> {self.place})'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Conferencia Publicada'
        verbose_name_plural = 'Listado de Conferencias Publicadas'


class UnpublishedLectures(GeneralFieldsOfModels):
    # Conferencias No Publicadas
    user = models.ManyToManyField(User, related_name='%(class)s')
    title = models.CharField(
        verbose_name='Título de Conferencia', null=False, blank=False, max_length=200)
    present = models.CharField(
        verbose_name='Lugar de Presentación de Conferencia',
        null=False, blank=False, max_length=200, default='')
    congress = models.CharField(
        verbose_name='Nombre de Congreso', null=True, max_length=200)
    city = models.CharField(verbose_name='Ciudad', null=True, max_length=50)
    country = models.CharField(verbose_name='País', null=True, max_length=50)
    institute = models.CharField(verbose_name='Institución', null=True, max_length=150)
    type_job = models.CharField(verbose_name='Tipo de Investigación', null=True, max_length=100)

    def __str__(self):
        return f'{self.pk}: {self.title[:40]} ({self.city} -> {self.congress})'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Conferencia No Publicada'
        verbose_name_plural = 'Listado de Conferencias no Publicadas'


class ResearchProjects(GeneralFieldsOfModels):
    # Proyectos de Investigación Aprox
    departament = models.ForeignKey(Departament, on_delete=models.CASCADE)
    name = models.CharField(
        verbose_name='Nombre de Proyecto', null=False, blank=False, max_length=255)
    participants = models.CharField(verbose_name='Participantes', null=True, max_length=255)
    approval = models.CharField(
        verbose_name='Fecha de Aprobación', null=False, blank=False, max_length=100)
    validity = models.CharField(verbose_name='Vigencia', null=True, max_length=100)
    section = models.CharField(verbose_name='Sesión de Consejo', null=True, max_length=50)
    means = models.CharField(verbose_name='Monto de Recursos', null=True, max_length=100)
    line = models.TextField(verbose_name='Líneas de Investigación', null=True)

    def __str__(self):
        return f'{self.pk}: {self.name[:100]} ({self.departament} -> {self.approval})'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Proyecto de Investigación'
        verbose_name_plural = 'Listado de Proyectos de Investigación'
