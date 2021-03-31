"""
Módulo de Acdemic Statisitcs para el proyecto DSCH
    actions:
        -> FileAcademicStatisticsView:
            * Registrar información desde un libro xlsx

        -> GeneralAcademicStatisticsViews:
            * MOdificación de funcion list
            * Esta será heredada por las vistas de Academics
            * reutilizar código

        -> AcademicStatisticsView:
            * Listado de registros en Academic Statistics
                - year
                - trimestre
                - plan de estudio
                - departamento

        -> AcademicStatisticsTotalsView:
            * Listado de promedios de Academics Statistics
                - year
                - plan de estudio
                - departamento

        -> CreateAcademicStaticsView:
            * Registrar un nuevo en Academics Statistics

        -> ListDepartamentView:
            * Listado de departamentos existentes

        -> ListStudyPlanView:
            * Listado de planes de estudios existentes
"""


from rest_framework import generics, status
from rest_framework.response import Response

from django.db.models import Q

from api.bases.views import AccessUserViews
from api.authentication.models import User, Profile

from .utils import min_max_year
from . import serializers
from .models import AcademicStatistics, AcademicStatisticsTotals, Departament, StudyPlan, Course


class FileAcademicStatisticsView(generics.GenericAPIView):
    serializer_class = serializers.FileDataAcademicStatistics

    def post(self, request, *args, **kwargs):
        # inicializar el serrializer
        serializer = self.get_serializer(data=request.data)

        # verificar que este valido (file)
        if serializer.is_valid():

            # verificar si el proceso regresa un True al finalizar
            if serializer.upload_book_excel(file=request.FILES['file'], plan_study=self.kwargs['plan_study']):
                return Response(
                    {'file': 'Upload Correct'}, status=status.HTTP_201_CREATED)

            # si el proceso regresa un Flase, se suspende el proceso
            return Response(
                {'file': 'Revise Información, se encontrarón registros duplicados'},
                status=status.HTTP_406_NOT_ACCEPTABLE)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GeneralAcademicStatisticsViews(generics.ListAPIView):

    def list(self, request, *args, **kwargs):
        # filtar la consulta e la BD
        queryset = self.filter_queryset(self.get_queryset())

        # si existe una o más coincidencias continúa el proceso
        if len(queryset) > 0:

            # se realiza una paginación
            page = self.paginate_queryset(queryset)

            # si existe una paginación
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            # si no existe paginación, pero si información
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        # no existen coincidencias
        return Response({'message': 'No hay coincidencias'},
                        status=status.HTTP_404_NOT_FOUND)


class AcademicStatisticsView(AccessUserViews, GeneralAcademicStatisticsViews):
    serializer_class = serializers.AcademicStatisticsSerializer

    def get_queryset(self):
        """
        :return: array de instancias obtenidas mediante un filtro por parametros enviados en URL
        """
        return AcademicStatistics.objects.filter(
            departament__name=self.kwargs['departament'],
            study_plan__name=self.kwargs['plan'],
            year=self.kwargs['year'],
            trimester=self.kwargs['trimester'])


class AcademicStatisticsTotalsView(AccessUserViews, GeneralAcademicStatisticsViews):
    serializer_class = serializers.AcademicStatisticsTotalSerializer

    def get_queryset(self):
        """
        :return: array de instancias obtenidas mediante un filtro por parametros enviados en URL
            """
        return AcademicStatisticsTotals.objects.filter(
            departament__name=self.kwargs['departament'],
            study_plan__name=self.kwargs['plan'],
            year=self.kwargs['year'])


class CreateAcademicStaticsView(AccessUserViews, generics.CreateAPIView):
    serializer_class = serializers.CreateAcademicStatisticsSerializer


class UpdateAcademicStaticsView(AccessUserViews, generics.UpdateAPIView):
    serializer_class = serializers.UpdateAcademicStatisticsSerializer
    queryset = AcademicStatistics.objects.all()

    def get_object(self):
        """
        :return: regresa una instancia del modelo AcademicStatics
        """
        try:
            obj = AcademicStatistics.objects.get(pk=self.kwargs['pk'])
            return obj

        except AcademicStatistics.DoesNotExist:
            return True

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # veriricar que la variable instance no sea boleana
        if not isinstance(instance, bool):

            # enviar instancia e información de usuario
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)

            # guardar modificaciones
            self.perform_update(serializer)

            # regresar instancia modificada
            return Response(serializer.data)


class RetrieveAcademicStaticsView(AccessUserViews, generics.RetrieveAPIView):
    serializer_class = serializers.UpdateAcademicStatisticsSerializer
    queryset = AcademicStatistics.objects.all()

    def get_object(self):
        """
        :return: regresa una instancia del modelo AcademicStatics
        """
        try:
            obj = AcademicStatistics.objects.get(pk=self.kwargs['pk'])
            return obj

        except AcademicStatistics.DoesNotExist:
            return True

    def retrieve(self, request, *args, **kwargs):
        # se obtiene la instacia a trabajar
        instance = self.get_object()

        # verificar si no es de tipo booleano
        if not isinstance(instance, bool):

            # enviar la instancia para obtener la información serializada
            serializer = self.get_serializer(instance)

            # regresar diccionario
            return Response(serializer.data)

        return Response({'detail': 'No Hay Coinicidencias'})


class ListHistoryAcademicForUser(AccessUserViews, GeneralAcademicStatisticsViews):
    serializer_class = serializers.UpdateAcademicStatisticsSerializer

    def get_object(self):
        # obtener el usuario en sesión por medio del token de autentificación
        return self.request.user

    def get_queryset(self):
        user = self.get_object()
        # obtener los registro existentes al usuario en sesión
        return AcademicStatistics.objects.filter(user=user)


class ListDepartamentView(AccessUserViews, generics.ListAPIView):
    serializer_class = serializers.DepartamentSerializer
    queryset = Departament.objects.all()


class ListStudyPlanView(AccessUserViews, generics.ListAPIView):
    serializer_class = serializers.StudyPlanSerializer
    queryset = StudyPlan.objects.all()


class ListYears(AccessUserViews, generics.ListAPIView):
    serializer_class = serializers.YearSerializer

    def get_queryset(self):
        query = min_max_year()
        return query


class ListHistoryAcademicForUserAndForYear(AccessUserViews, GeneralAcademicStatisticsViews):
    serializer_class = serializers.HistoryAcademicStatisticForUsersSerializer

    def get_object(self):
        # obtener el usuario en sesión por medio del token de autentificación
        return self.request.user

    def get_queryset(self):
        user = self.get_object()
        # obtener los registro existentes al usuario en sesión
        return AcademicStatistics.objects.filter(user=user, year=self.kwargs['year'])


class CourseView(AccessUserViews, GeneralAcademicStatisticsViews):
    serializer_class = serializers.CourseSerializer

    def get_queryset(self):
        if self.kwargs['filter'] == '1':
            return Course.objects.all()[:20]

        return Course.objects.filter(name__istartswith=self.kwargs['filter'])

    def list(self, request, *args, **kwargs):
        # filtar la consulta e la BD
        queryset = self.filter_queryset(self.get_queryset())

        # si existe una o más coincidencias continúa el proceso
        if len(queryset) > 0:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        return Response(status=status.HTTP_404_NOT_FOUND)


class AcademicStatisticsFilterCourseView(AccessUserViews, GeneralAcademicStatisticsViews):
    serializer_class = serializers.AcademicStatisticsTotalSerializer

    def get_queryset(self):
        """
        :return: array de instancias obtenidas mediante un filtro por parametros enviados en URL
        """
        try:
            user = User.objects.get(number=self.kwargs['number'])

        except User.DoesNotExist:

            return []

        academics = AcademicStatistics.objects.filter(
            course__name__icontains=self.kwargs['course'], user__number=self.kwargs['number'])
        list_totals = list()

        for academic in academics:
            list_totals.append(academic.totals)

        return list_totals


class ListTotalsMultiPlans(AccessUserViews, generics.ListAPIView):
    serializer_class = serializers.AcademicStatisticsTotalSerializer

    def get_queryset(self):
        list_query = list()
        list_plans = self.kwargs['plans'].split('-')
        print(list_plans)

        for plan in list_plans:
            if len(plan) > 1:
                objs = AcademicStatisticsTotals.objects.filter(
                    study_plan__name=plan,
                    departament__name=self.kwargs['departament'],
                    year__range=(self.kwargs['initial'], self.kwargs['final'])
                )

                for obj in objs:
                    list_query.append(obj)

        return list_query

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if len(queryset) > 0:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        return Response({'message': 'No hay coincidencias'}, status=status.HTTP_404_NOT_FOUND)


class UserPrivilegesAcademicView(AccessUserViews, generics.GenericAPIView):
    serializer_class = serializers.UserPrivilegesAcademicSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            instance = serializer.create(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeletePrivilegeUserView(AccessUserViews, generics.DestroyAPIView):
    serializer_class = None
    queryset = Profile.objects.none()

    def get_object(self):
        try:
            return Profile.objects.get(pk=self.kwargs['pk'])
        except Profile.DoesNotExist:
            return None

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance is not None:
            instance.departament = 'admin_null'
            instance.save()
            return Response({'message': 'Permiso Eliminado'}, status=status.HTTP_200_OK)

        return Response({'message': 'NO existe Usuario'}, status=status.HTTP_400_BAD_REQUEST)


class ListUserPrivilegesAcademicView(AccessUserViews, generics.ListAPIView):
    serializer_class = serializers.UserPrivilegesSerializer

    def get_queryset(self):
        return Profile.objects.filter(
            Q(departament='view_academic_humanities') |
            Q(departament='view_academic_social_sciences') |
            Q(departament='view_academic_institutional_studies')
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
