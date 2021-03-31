from rest_framework import serializers
from django.db.models import Q

from api.authentication.models import Profile, User
from api.academic.models import Departament
from api.authentication.serializers import UserSerializer

from .utils import ProcessFileXLSX
from .process import SaveDataToFile
from . import models

import zipfile
import openpyxl


class AddFileSerializer(serializers.Serializer, ProcessFileXLSX, SaveDataToFile):
    file = serializers.FileField(required=True)
    year = serializers.IntegerField(required=True)

    @staticmethod
    def get_type_report(title):
        instance, created = models.TypeReport.objects.get_or_create(name=title)
        print(instance, created)
        return instance

    @staticmethod
    def check_exists_annual_report(year):
        return models.AnnualReport.objects.get_or_create(year=year)

    @staticmethod
    def get_departament(departament):
        instance, created = Departament.objects.get_or_create(name=departament)
        print(instance, created)
        return instance

    @staticmethod
    def get_user(user):
        list_user = user.split(' ')
        if len(list_user) >= 3:
            instance = Profile.objects.filter(
                Q(name__unaccent__icontains=list_user[-1])
                &
                (
                    Q(paternal_surname__unaccent__icontains=list_user[0])
                    |
                    Q(maternal_surname__unaccent__icontains=list_user[1])
                )
            )

        elif len(list_user) == 2:
            instance = Profile.objects.filter(
                Q(name__unaccent__icontains=list_user[1])
                &
                (
                    Q(paternal_surname__unaccent__icontains=list_user[0])
                    |
                    Q(maternal_surname__unaccent__icontains=list_user[0])
                )
            )

        if len(instance) > 0:
            return instance[0]

        return None

    def get_users(self, list_user):
        list_profile = list()
        list_user = list_user.split(',')

        for user in list_user:
            profile = self.get_user(user.strip())

            if profile is not None:
                list_profile.append(profile)

            else:
                pass

        return list_profile

    def process_data(self, list_rows, page, annual_report):
        type_report = self.get_type_report(page)

        for row in list_rows[1:]:
            if page == 'Actualización y formación docen':
                profile = self.get_user(row[0])

                if profile is None:
                    print('Usuario No encontrado: ', row[0])

                else:
                    self.save_teacher_training(annual_report, type_report, profile.user, row)

            elif page == 'Actividad de intercambio':
                profile = self.get_user(row[0])

                if profile is None:
                    print('Usuario No encontrado: ', row[0])

                else:
                    self.save_exchange_activity(annual_report, type_report, profile.user, row)

            elif page == 'Eventos acádemicos':
                profile = self.get_user(row[0])

                if profile is None:
                    print('Usuario No encontrado: ', row[0])

                else:
                    self.save_academic_events(annual_report, type_report, profile.user, row)

            elif page == 'Redes colaboración acádemica':
                profile = self.get_user(row[0])

                if profile is None:
                    print('Usuario No encontrado: ', row[0])

                else:
                    self.save_academic_collaboration(annual_report, type_report, profile.user, row)

            elif page == 'Colaboración proyectos':
                profile = self.get_user(row[0])

                if profile is None:
                    print('Usuario No encontrado: ', row[0])

                else:
                    self.save_project_collaboration(annual_report, type_report, profile.user, row)

            elif page == 'Publicaciones revistas':
                list_users = self.get_users(row[0])

                if len(list_users) > 0:
                    self.save_magazine_publications(annual_report, type_report, list_users, row)

            elif page == 'Revistas electrónicas':
                list_users = self.get_users(row[0])

                if len(list_users):
                    self.save_electronic_journals(annual_report, type_report, list_users, row)

            elif page == 'Publicaciones periódicos':
                list_users = self.get_users(row[0])

                if len(list_users) > 0:
                    self.save_newspaper_publication(annual_report, type_report, list_users, row)

            elif page == 'Libros publicados':
                list_users = self.get_users(row[0])

                if len(list_users) > 0:
                    self.save_published_books(annual_report, type_report, list_users, row)

            elif page == 'Capítulos de libros':
                list_users = self.get_users(row[1])

                if len(list_users) > 0:
                    departament = self.get_departament(row[0])
                    self.save_chapters_books(annual_report, type_report, list_users, departament, row)

            elif page == 'Reseñas de libros':
                profile = self.get_user(row[0])

                if profile is None:
                    print('Usuario No encontrado: ', row[0])

                else:
                    self.save_book_reviews(annual_report, type_report, profile.user, row)

            elif page == 'Conferencias publicadas':
                list_users = self.get_users(row[0])

                if len(list_users) > 0:
                    self.save_published_lectures(annual_report, type_report, list_users, row)

            elif page == 'Conferencias no publicadas':
                list_users = self.get_users(row[0])

                if len(list_users) > 0:
                    self.save_unpublished_lectures(annual_report, type_report, list_users, row)

            elif page == 'Proyectos investigación apro':
                profile = self.get_user(row[2])

                if profile is None:
                    print('Usuario No encontrado: ', row[2])

                else:
                    departament = self.get_departament(row[0])
                    self.save_research_projects(
                        annual_report, type_report, profile.user, departament, row)

        return True

    def read_file(self, file, validated_data):
        try:
            book = openpyxl.load_workbook(file)
            pages = book.get_sheet_names()

        except KeyError:
            return None

        except zipfile.BadZipFile:
            return None

        except OSError:
            return None

        annual_report, created = self.check_exists_annual_report(validated_data.get('year'))
        if not created:
            return created

        count = 0
        for page in pages:
            data = book.get_sheet_by_name(page)
            list_rows = self.separate_rows_from_pages(data)
            list_rows = self.clean_data(list_rows)
            result = self.process_data(list_rows, page, annual_report)

            if count == 6:
                return result

            count += 1

        return True


class TypeReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TypeReport
        fields = '__all__'


class GeneralProductionSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'


class GeneralProductionOneUserSerializer(GeneralProductionSerializer):

    @staticmethod
    def get_profile(attrs):
        return UserSerializer(attrs.user.profile).data


class GeneralProductionManyUserSerializer(GeneralProductionSerializer):

    @staticmethod
    def get_profile(attrs):
        users = [user.profile for user in attrs.user.all()]
        return UserSerializer(users, many=True).data


class TeacherTrainingSerializer(GeneralProductionOneUserSerializer):

    class Meta(GeneralProductionOneUserSerializer.Meta):
        model = models.TeacherTraining


class ExchangeActivitySerializer(GeneralProductionOneUserSerializer):

    class Meta(GeneralProductionOneUserSerializer.Meta):
        model = models.ExchangeActivity


class AcademicEventsSerializer(GeneralProductionOneUserSerializer):

    class Meta(GeneralProductionOneUserSerializer.Meta):
        model = models.AcademicEvents


class AcademicCollaborationSerializer(GeneralProductionOneUserSerializer):

    class Meta(GeneralProductionOneUserSerializer.Meta):
        model = models.AcademicCollaboration


class ProjectCollaborationSerializer(GeneralProductionOneUserSerializer):

    class Meta(GeneralProductionOneUserSerializer.Meta):
        model = models.ProjectCollaboration


class MagazinePublicationsSerializer(GeneralProductionManyUserSerializer):

    class Meta(GeneralProductionManyUserSerializer.Meta):
        model = models.MagazinePublications


class ElectronicJournalsSerializer(GeneralProductionManyUserSerializer):

    class Meta(GeneralProductionManyUserSerializer.Meta):
        model = models.ElectronicJournals


class NewspaperPublicationSerializer(GeneralProductionManyUserSerializer):

    class Meta(GeneralProductionManyUserSerializer.Meta):
        model = models.NewspaperPublication


class PublishedBooksSerializer(GeneralProductionManyUserSerializer):

    class Meta(GeneralProductionManyUserSerializer.Meta):
        model = models.PublishedBooks


class ChaptersBooksSerializer(GeneralProductionManyUserSerializer):
    departament = serializers.CharField()

    class Meta(GeneralProductionManyUserSerializer.Meta):
        model = models.ChaptersBooks


class BookReviewsSerializer(GeneralProductionOneUserSerializer):

    class Meta(GeneralProductionOneUserSerializer.Meta):
        model = models.BookReviews


class PublishedLecturesSerializer(GeneralProductionManyUserSerializer):

    class Meta(GeneralProductionManyUserSerializer.Meta):
        model = models.PublishedLectures


class UnpublishedLecturesSerializer(GeneralProductionManyUserSerializer):

    class Meta(GeneralProductionManyUserSerializer.Meta):
        model = models.UnpublishedLectures
        fields = '__all__'


class ResearchProjectsSerializer(GeneralProductionOneUserSerializer):
    departament = serializers.CharField()

    class Meta(GeneralProductionOneUserSerializer.Meta):
        model = models.ResearchProjects
