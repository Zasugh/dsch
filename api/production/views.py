from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q

from . import serializers
from . import models


class AddFileView(generics.CreateAPIView):
    serializer_class = serializers.AddFileSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            result = serializer.read_file(
                file=request.FILES['file'], validated_data=serializer.data)

            if result is not None:

                if result:
                    return Response(
                        {'msg', 'Información Almacenada Correctamente'},
                        status=status.HTTP_201_CREATED)

                year = serializer.data.get('year')
                return Response(
                    {'detail': 'Ya existe un Reporte del año {}'.format(year)},
                    status=status.HTTP_406_NOT_ACCEPTABLE)

            return Response(
                {'detail': 'Archivo No compatible'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListTypeReportView(generics.ListAPIView):
    serializer_class = serializers.TypeReportSerializer

    def get_queryset(self):
        return models.TypeReport.objects.all()


class ProductionGeneralListView(generics.ListAPIView):
    serializer_class = None

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if len(queryset) > 0:
            return Response(self.get_serializer(queryset, many=True).data, status.HTTP_202_ACCEPTED)

        return Response(status=status.HTTP_200_OK)


class TeacherTrainingListView(ProductionGeneralListView):
    serializer_class = serializers.TeacherTrainingSerializer

    def get_queryset(self):
        return models.TeacherTraining.objects.filter(
            annual_report__year=self.kwargs['year'],
            institute__icontains=self.kwargs['institute'])


class ExchangeActivityListView(ProductionGeneralListView):
    serializer_class = serializers.ExchangeActivitySerializer

    def get_queryset(self):
        return models.ExchangeActivity.objects.filter(
            Q(annual_report__year=self.kwargs['year'])
            &
            (
                Q(division__icontains=self.kwargs['division'])
                |
                Q(ies__icontains=self.kwargs['ies'])
            )
        )


class AcademicEventsListView(ProductionGeneralListView):
    serializer_class = serializers.AcademicEventsSerializer

    def get_queryset(self):
        return models.AcademicEvents.objects.filter(
            Q(annual_report__year=self.kwargs['year'])
            &
            (
                Q(type_activity__icontains=self.kwargs['activity'])
                |
                Q(range_date__icontains=self.kwargs['month'])
            )
        )


class AcademicCollaborationListView(ProductionGeneralListView):
    serializer_class = serializers.AcademicCollaborationSerializer

    def get_queryset(self):
        return models.AcademicCollaboration.objects.filter(
            Q(annual_report__year=self.kwargs['year'])
            &
            Q(institutions__icontains=self.kwargs['institutions'])
        )


class ProjectCollaborationView(ProductionGeneralListView):
    serializer_class = serializers.ProjectCollaborationSerializer

    def get_queryset(self):
        sector = None

        if self.kwargs['sector'] == 3:
            return models.ProjectCollaboration.objects.all()

        elif self.kwargs['sector'] == 2:
            sector = 'Público'

        elif self.kwargs['sector'] == 1:
            sector = 'Privado'

        return models.ProjectCollaboration.objects.filter(
            annual_report__year=self.kwargs['year'], sector=sector)


class MagazinePublicationsListView(ProjectCollaborationView):
    serializer_class = serializers.MagazinePublicationsSerializer

    def get_queryset(self):
        index, act_type = 'No', 'investiga'

        if self.kwargs['index'] == 1:
            index = 'Sí'

        if self.kwargs['type'] == 2:
            act_type = 'divulga'

        return models.MagazinePublications.objects.filter(
            annual_report__year=self.kwargs['year'],
            is_indexed_magazine__icontains=index,
            type_job__icontains=act_type
        )


class ElectronicJournalsListView(ProductionGeneralListView):
    serializer_class = serializers.ElectronicJournalsSerializer

    def get_queryset(self):
        act_type = 'investiga'

        if self.kwargs['type'] == 2:
            act_type = 'divulga'

        return models.ElectronicJournals.objects.filter(
            annual_report__year=self.kwargs['year'],
            type_job__icontains=act_type,
            magazine_name__icontains=self.kwargs['name']
        )


class NewspaperPublicationListView(ProductionGeneralListView):
    serializer_class = serializers.NewspaperPublicationSerializer

    def get_queryset(self):
        return models.NewspaperPublication.objects.filter(
            annual_report__year=self.kwargs['year'],
            newspaper_name__icontains=self.kwargs['name']
        )


class PublishedBooksListView(ProductionGeneralListView):
    serializer_class = serializers.PublishedBooksSerializer

    def get_queryset(self):
        act_type = 'investiga'

        if self.kwargs['type'] == 2:
            act_type = 'divulga'

        return models.PublishedBooks.objects.filter(
            annual_report__year=self.kwargs['year'],
            type_job__icontains=act_type,
            editorial__icontains=self.kwargs['editorial']
        )


class ChaptersBooksListView(ProductionGeneralListView):
    serializer_class = serializers.ChaptersBooksSerializer

    def get_queryset(self):
        return models.ChaptersBooks.objects.filter(
            annual_report__year=self.kwargs['year'],
            name__icontains=self.kwargs['title']
        )


class BookReviewsListView(ProductionGeneralListView):
    serializer_class = serializers.BookReviewsSerializer

    def get_queryset(self):
        return models.BookReviews.objects.filter(
                annual_report__year=self.kwargs['year'])


class PublishedLecturesListView(ProductionGeneralListView):
    serializer_class = serializers.PublishedLecturesSerializer

    def get_queryset(self):
        if self.kwargs['type'] == 1:
            type_temp = 'Conferencia'

        elif self.kwargs['type'] == 2:
            type_temp = 'Conferencia magistral'

        elif self.kwargs['type'] == 3:
            type_temp = 'Trabajo en evento'

        else:
            return models.PublishedLectures.objects.all()

        return models.PublishedLectures.objects.filter(
            annual_report__year=self.kwargs['year'],
            type_job=type_temp
        )


class UnpublishedLecturesListView(ProductionGeneralListView):
    serializer_class = serializers.UnpublishedLecturesSerializer

    def get_queryset(self):
        if self.kwargs['type'] == 1:
            type_temp = 'Conferencia'

        elif self.kwargs['type'] == 2:
            type_temp = 'Conferencia magistral'

        elif self.kwargs['type'] == 3:
            type_temp = 'Trabajo en evento'

        return models.UnpublishedLectures.objects.filter(
            annual_report__year=self.kwargs['year'],
            type_job=type_temp,
            institute__icontains=self.kwargs['institute']

        )


class ResearchProjectsListView(ProductionGeneralListView):
    serializer_class = serializers.ResearchProjectsSerializer

    def get_queryset(self):
        return models.ResearchProjects.objects.filter(
            annual_report__year=self.kwargs['year'],
            departament__name__istartswith=self.kwargs['departament']
        )
