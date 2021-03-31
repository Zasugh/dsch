"""
Módulo de Academic Statistics para el proyecto DSCH
    actions serializers:
        -> FileDataAcademicStatistics
            * upload_book_excel     -> leé el archivo xlsx y procesa la información del libro
            * receiver_data         -> recibe la información procesa de una página
            * search_user           -> busca la instancia del usuario al que pertenece la información
                                       a alamacenar
            * search_plan           -> busca la instancia del plan de estudios a registrar
            * search_departament    -> busca la instancia de departamento a registrar
            * register_data_file    -> registra la información

        -> AcademicStatisticsSerializer
            * Visualizar información existente mediante el siguiente filtro:
                - año
                - trimestre
                - departamento
                - plan de estudios

        -> AcademicStatisticsTotalSerializer
            * Visualizar información de lso totales existente mediante el siguiente filtro:
                - año
                - departamento
                - plan de estudios

        -> CreateAcademicStatisticsSerializer
            * create                -> registra la información recibida
            * verified_exist        -> verifica que no exista un registro igual:
                                        - año
                                        - departament
                                        - trimestre
                                        - plan de estudios
            * assign_totals         -> asigna la instancia del total a la instancia actual

        -> DepartamentSerializer:
            * Visualizar todos los departamentos existentes

        -> StudyPlanSerializer:
            * Visualizar todos los planes de estudios existentes

"""


from rest_framework import serializers

from django.db.models import Q
from django.apps import apps

from .models import AcademicStatistics, Departament, StudyPlan, AcademicStatisticsTotals, User, Course
from api.authentication.models import Profile

import openpyxl


class FileDataAcademicStatistics(serializers.Serializer):
    """
    campos de solo lectura:
        * file -> es requerido
    otros campos iniciales:
        - Profile -> Modelo de Perfil
        - User -> Modelo de Usuarios
    """
    file = serializers.FileField(write_only=True, required=True)
    Profile = apps.get_model('authentication', 'Profile')
    User = apps.get_model('authentication', 'User')
    number_temp = 0
    exists_year = False
    year = 0

    def upload_book_excel(self, file, plan_study):
        """
        :param file: archivo almacenado en la menoria temporal
        :return: valor booleano
        """

        # cargar el archivo en una variable
        book = openpyxl.load_workbook(file)

        # obtener los nombre las hojas existentes en le libro
        pages = book.get_sheet_names()
        # separar las paginas del libreo
        for page in pages:
            # almacenarán las variables permitenetes de acuerdo a la pagina
            plan, departament, year = '', '', 0

            # almacenará las filas de la página
            list_rows = list()

            # separar la información por celdas
            data = book.get_sheet_by_name(page)

            # separar columnas el la informacion obtenida
            for row in data.iter_rows():
                temp_row = self.process_row_to_list(row=row)

                if len(temp_row) > 0:
                    list_rows.append(temp_row)

            list_rows = self.process_rows(list_rows)

            if len(list_rows) > 0:
                option = self.process_data(
                    list_rows, departament=page, plan_study=plan_study, year=self.year)

                if not option:
                    return option

            else:
                return False

        return True

    def search_user(self, user):
        try:
            instance = self.User.objects.get(number=user)
        except User.DoesNotExist:
            instance = None
        return instance

    @staticmethod
    def search_departament(departament):
        instance, verified = Departament.objects.get_or_create(name=departament)
        return instance

    @staticmethod
    def search_plan(plan):
        try:
            return StudyPlan.objects.get(name=plan)

        except StudyPlan.DoesNotExist:
            return None

    @staticmethod
    def create_course(course):
        course, verified = Course.objects.get_or_create(name=course)
        return course

    @staticmethod
    def separate_row(row):
        list_rows = list()
        initial, final = 0, 4
        for x in range(6):
            list_rows.append(row[initial: final])
            initial = final
            final += 4
        # return [row[:4], row[4:8], row[8:12], row[12:16], row[16:20], row[20:24]]
        return list_rows

    def process_data(self, rows: list = [], departament: str = '', plan_study: int = 1, year: int = 0):
        index_count = 2
        list_users = list()
        trimesters = ['Invierno', 'Primavera', 'Otoño']

        for row in rows:
            row_temp = row[2:]
            list_temp = self.separate_row(row_temp)
            position_list_initial = 0
            in_classroom = bool

            for position in range(3):
                for register in range(2):
                    if register == 0:
                        in_classroom = True
                    else:
                        in_classroom = False

                    if list_temp[position_list_initial][0] is not None:

                        plan_study_option = self.search_plan(plan_study)
                        if plan_study_option is None:
                            return False

                        instance_plan_study = plan_study_option
                        instance_user = self.search_user(row[0])
                        instance_departament = self.search_departament(departament)
                        instance_course = self.create_course(list_temp[position_list_initial][0])

                        if instance_user is None:
                            if row[0] not in list_users:
                                list_users.append(row[0])
                            # raise serializers.ValidationError('Usuario No Existe')
                            continue

                        option, group_actual = self.verify_exists_data(
                            trimesters[position], instance_user, instance_plan_study,
                            instance_departament, instance_course, year, in_classroom
                        )

                        if not option and instance_departament is not None:
                            print('registro', year, instance_plan_study, instance_departament, instance_user)

                            academic = AcademicStatistics.objects.create(
                                number_course=float(list_temp[position_list_initial][1]),
                                number_hour=float(list_temp[position_list_initial][2]),
                                number_student=float(list_temp[position_list_initial][3]),
                                classroom=in_classroom,
                                trimester=trimesters[position],
                                year=year,
                                user=instance_user,
                                study_plan=instance_plan_study,
                                departament=instance_departament,
                                course=instance_course,
                                number_group=group_actual
                            )

                            totals, verified = AcademicStatisticsTotals.objects.get_or_create(
                                year=year,
                                user=instance_user,
                                study_plan=instance_plan_study,
                                departament=instance_departament
                            )

                            academic.totals = totals
                            academic.save()

                        else:
                            # return False
                            continue

                    position_list_initial += 1

        print(list_users)
        return True

    @staticmethod
    def verify_exists_data(trimester, user, study_plan, departament, course, year, classroom):
        group = 1

        for x in range(2):
            instances = AcademicStatistics.objects.filter(
                trimester=trimester, user=user, study_plan=study_plan,
                departament=departament, course=course, year=year,
                classroom=classroom, number_group=group
            )

            if not instances.exists():
                return False, group

            else:
                group = 2

        return True, group

    @staticmethod
    def process_rows(rows: list = []):
        new_rows = list()
        for row in rows:
            try:
                if row[0] is not None:
                    if isinstance(row[0], int):
                        new_rows.append(row[:26])
            except IndexError:
                return []
        return new_rows

    def process_row_to_list(self, row: list = []):
        # reparar la celdas de la filas
        list_row = list()

        for cell in row:
            if not self.exists_year:
                if cell.value is not None:
                    self.select_year(cell.value)
            else:
                if row[0].value is not None:
                    list_row.append(cell.value)
                # self.process_data(cell=cell, departament=departament, plan_study=plan_study)
        return list_row

    def select_year(self, string: str):
        parser = string.split(' ')
        for option in parser:
            if option.isdigit():
                self.exists_year = True
                self.year = int(option)
                break


class AcademicStatisticsSerializer(serializers.ModelSerializer):
    """
    campos de solo lectura:
        * todos
    """
    user = serializers.CharField()
    study_plan = serializers.CharField()
    departament = serializers.CharField()
    course = serializers.CharField()
    name = serializers.SerializerMethodField()

    @staticmethod
    def get_name(attrs):
        return attrs.user.profile.get_full_name().title()

    class Meta:
        model = AcademicStatistics
        fields = '__all__'


class AcademicStatisticsTotalSerializer(serializers.ModelSerializer):
    """
    campos de solo lectura:
        * todos
    """
    user = serializers.CharField()
    totals_course = serializers.SerializerMethodField()
    totals_hour = serializers.SerializerMethodField()
    totals_student = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    @staticmethod
    def get_name(attrs):
        return attrs.user.profile.get_full_name().title()

    @staticmethod
    def get_totals_course(attrs):
        totals_course = attrs.course_in_classroom + attrs.course_out_classroom
        return totals_course

    @staticmethod
    def get_totals_hour(attrs):
        totals_hour = attrs.hour_in_classroom + attrs.hour_out_classroom
        return totals_hour

    @staticmethod
    def get_totals_student(attrs):
        totals_student = attrs.student_in_classroom + attrs.student_out_classroom
        return totals_student

    class Meta:
        model = AcademicStatisticsTotals
        fields = '__all__'


class CreateAcademicStatisticsSerializer(serializers.ModelSerializer):
    """
    campos de solo lectura:
        * todos

    campos de solo escritura:
        * course_in_classroom               * hour_in_classroom
        * student_in_classroom              * course_out_classroom
        * hour_out_classroom                * student_out_classroom
        * trimester                         * year
        * user                              * study_plan
        * departament
    """
    user = serializers.CharField()
    study_plan = serializers.CharField()
    departament = serializers.CharField()
    course = serializers.CharField()

    @staticmethod
    def instance_course(validated_data):
        instance, verified = Course.objects.get_or_create(name=validated_data.get('course'))
        return instance

    def create(self, validated_data):
        """
        :param validated_data: información a almacenar

        :return: instance
        """

        # Generar las instancias para almacenar la inforamción
        validated_data = self.get_instance(validated_data)

        # verificar no exista un registro con la misma información enviada
        if self.verified_exist(validated_data):
            course_instance = self.instance_course(validated_data)

            # almacenara la información
            instance = AcademicStatistics.objects.create(
                number_course=validated_data.get('number_course'),
                number_hour=validated_data.get('number_hour'),
                number_student=validated_data.get('number_student'),
                classroom=validated_data.get('classroom'),
                trimester=validated_data.get('trimester'),
                year=validated_data.get('year'),
                user=validated_data.get('user'),
                study_plan=validated_data.get('study_plan'),
                departament=validated_data.get('departament'),
                totals=self.assign_totals(validated_data),
                course=self.instance_course(validated_data)
            )
            # guardar la instancia
            instance.save()
            return instance

        else:
            raise serializers.ValidationError('Verifique Información, ya existe un registro igual')

    @staticmethod
    def get_instance(validated_data):
        try:
            user = User.objects.get(number=validated_data['user'])
            study_plan = StudyPlan.objects.get(name=validated_data['study_plan'])
            departament = Departament.objects.get(name=validated_data['departament'])

        except User.DoesNotExist:
            raise serializers.ValidationError('Número Económico No existe')

        validated_data['user'] = user
        validated_data['study_plan'] = study_plan
        validated_data['departament'] = departament
        return validated_data

    @staticmethod
    def verified_exist(validated_data):
        """
        :param validated_data: información a almacenar

        :return: valor boolean
        """

        # filtar regristro con la información acutal
        instance = AcademicStatistics.objects.filter(
            trimester=validated_data.get('trimester'),
            year=validated_data.get('year'),
            user=validated_data.get('user'),
            study_plan=validated_data.get('study_plan'),
            departament=validated_data.get('departament'),
            course__name=validated_data.get('course'),
            classroom=validated_data.get('classroom')
        )

        # si el filtro es mayor a 0, detener para evitar duplicidad
        if len(instance) > 0:
            return False

        return True

    @staticmethod
    def assign_totals(validated_data):
        """
        :param validated_data: información a almacenar
        :return: instance
        """

        # crear o obtener la instancia de seguimiento de totales, de acuerdo a la información acutal
        totals, verified = AcademicStatisticsTotals.objects.get_or_create(
            year=validated_data.get('year'),
            user=validated_data.get('user'),
            study_plan=validated_data.get('study_plan'),
            departament=validated_data.get('departament'))

        return totals

    class Meta:
        model = AcademicStatistics
        exclude = ['totals', 'created_at']


class DepartamentSerializer(serializers.ModelSerializer):
    """
    campos de visualización:
        * id
        * name
    """

    class Meta:
        model = Departament
        fields = ['id', 'name']


class StudyPlanSerializer(serializers.ModelSerializer):
    """
    campos de visualización:
        * id
        * name
    """

    class Meta:
        model = StudyPlan
        fields = ['id', 'name']


class YearSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    year = serializers.CharField(read_only=True)


class UpdateAcademicStatisticsSerializer(serializers.ModelSerializer):
    trimester = serializers.CharField(read_only=True)
    year = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    user = serializers.CharField(read_only=True)
    study_plan = serializers.CharField(read_only=True)
    departament = serializers.CharField(read_only=True)
    course = serializers.CharField(read_only=True)

    def update(self, instance, validated_data):
        """
        :param instance: instacia a modificar en la operación
        :param validated_data: información a agregar
        :return:
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    class Meta:
        model = AcademicStatistics
        exclude = ['totals', ]


class HistoryAcademicStatisticForUsersSerializer(serializers.ModelSerializer):
    trimester = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    study_plan = serializers.CharField(read_only=True)
    departament = serializers.CharField(read_only=True)
    full_name = serializers.SerializerMethodField()
    course = serializers.CharField(read_only=True)

    @staticmethod
    def get_full_name(attrs):
        instance = Profile.objects.get(user=attrs.user)
        return instance.get_full_name()

    class Meta:
        model = AcademicStatistics
        fields = '__all__'


class CourseSerializer (serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'


class UserPrivilegesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'


class UserPrivilegesAcademicSerializer(serializers.Serializer):
    privilege = serializers.IntegerField(required=True)
    number = serializers.CharField(required=True)

    @staticmethod
    def get_instance(number):
        return Profile.objects.get(user__number=number)

    def validate(self, attrs):
        msg = {'message': 'Ya existe un Usuario con ese permiso'}
        user = User.objects.filter(number=attrs.get('number'))

        if not user.exists():
            raise serializers.ValidationError({'message': 'Usuario no existe'})

        if attrs.get('privilege') == 1:
            profile = Profile.objects.filter(departament='view_academic_humanities')

            if profile.exists():
                raise serializers.ValidationError(msg)

        elif attrs.get('privilege') == 2:
            profile = Profile.objects.filter(departament='view_academic_social_sciences')

            if profile.exists():
                raise serializers.ValidationError(msg)

        elif attrs.get('privilege') == 3:
            profile = Profile.objects.filter(departament='view_academic_institutional_studies')

            if profile.exists():
                raise serializers.ValidationError(msg)

        else:
            pass

        return super().validate(attrs)

    def create(self, validated_data):
        instance = self.get_instance(validated_data.get('number'))

        if instance is not None:
            if validated_data.get('privilege') == 1:
                instance.departament = 'view_academic_humanities'

            elif validated_data.get('privilege') == 2:
                instance.departament = 'view_academic_social_sciences'

            elif validated_data.get('privilege') == 3:
                instance.departament = 'view_academic_institutional_studies'

            else:
                pass

            instance.save()
            return instance
