from django.db.models import signals
from django.dispatch import receiver

from .models import TypeReport


@receiver(signal=signals.post_migrate)
def create_types_report(**kwargs):
    a = TypeReport.objects.get_or_create(name='Actualización y formación docen')
    b = TypeReport.objects.get_or_create(name='Actividad de intercambio')
    c = TypeReport.objects.get_or_create(name='Eventos acádemicos')
    d = TypeReport.objects.get_or_create(name='Redes colaboración acádemica')
    e = TypeReport.objects.get_or_create(name='Colaboración proyectos')
    f = TypeReport.objects.get_or_create(name='Publicaciones revistas')
    g = TypeReport.objects.get_or_create(name='Revistas electrónicas')
    h = TypeReport.objects.get_or_create(name='Publicaciones periódicos')
    i = TypeReport.objects.get_or_create(name='Libros publicados')
    j = TypeReport.objects.get_or_create(name='Capítulos de libros')
    k = TypeReport.objects.get_or_create(name='Reseñas de libros')
    m = TypeReport.objects.get_or_create(name='Conferencias publicadas')
    n = TypeReport.objects.get_or_create(name='Conferencias no publicadas')
    o = TypeReport.objects.get_or_create(name='Proyectos investigación apro')

    print(a)
    print(b)
    print(c)
    print(d)
    print(e)
    print(f)
    print(g)
    print(h)
    print(i)
    print(j)
    print(k)
    print(m)
    print(n)
    print(o)
