from rest_framework import serializers

from api.authentication.models import User

from .models import ScholarShip, OptionRequest, AdditionalFiles
from api.authentication.models import Profile


class ScholarshipSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    full_name = serializers.SerializerMethodField()

    @staticmethod
    def get_full_name(attrs):
        name = Profile.objects.get(user__number=attrs.user)
        return name.get_full_name()

    class Meta:
        model = ScholarShip
        fields = '__all__'


class OptionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionRequest
        fields = '__all__'


class RequestScholarshipSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(required=True)
    date_send_request = serializers.DateTimeField(required=True)
    file_request = serializers.FileField(write_only=True)
    year = serializers.IntegerField(read_only=True, required=False)
    promotion = serializers.BooleanField(required=True)
    stimulus = serializers.BooleanField(required=True)
    trajectory = serializers.BooleanField(required=True)
    permanence = serializers.BooleanField(required=True)
    years = serializers.IntegerField(required=True)

    def validate(self, attrs):
        exist = User.objects.filter(number=attrs.get('user')).exists()

        if not exist:
            raise serializers.ValidationError('No existe Número Económico')

        cod = ScholarShip.objects.filter(number_request=attrs.get('number_request')).exists()

        if cod:
            raise serializers.ValidationError(
                'Ya existe un registro con el código enviado')

        return super().validate(attrs)

    @staticmethod
    def search_user(number):
        return User.objects.get(number=number)

    @staticmethod
    def get_year(date):
        dates = date.split('-')
        return dates[0]

    @staticmethod
    def get_years_permanence(year, permanence):
        if permanence:
            return year
        return 0

    def create(self, validated_data, url):
        instance = ScholarShip(
            user=self.search_user(validated_data.get('user')),
            date_request=validated_data.get('date_request'),
            number_request=validated_data.get('number_request'),
            file_request=url,
            date_send_request=validated_data.get('date_send_request'),
            year=self.get_year(validated_data.get('date_request')),
            promotion=validated_data.get('promotion'),
            stimulus=validated_data.get('stimulus'),
            trajectory=validated_data.get('trajectory'),
            permanence=validated_data.get('permanence'),
            years=self.get_years_permanence(validated_data.get('years'), validated_data.get('permanence'))
        )
        instance.save()
        return instance

    class Meta:
        model = ScholarShip
        fields = [
            'user', 'date_request', 'number_request', 'year', 'promotion', 'stimulus', 'trajectory',
            'file_request', 'date_send_request', 'permanence', 'years']


class DictumScholarshipSerializer(serializers.ModelSerializer):
    file_dictum = serializers.FileField(required=True, write_only=True)

    def validate(self, attrs):
        cod = ScholarShip.objects.filter(number_dictum=attrs.get('number_dictum')).exists()

        if cod:
            raise serializers.ValidationError('Ya existe un registro con el código enviado')

        return super().validate(attrs)

    @staticmethod
    def get_instance(pk):
        try:
            return ScholarShip.objects.get(pk=pk)

        except ScholarShip.DoesNotExist:
            raise serializers.ValidationError('NO HAY COINCIDENCIAS')

    def update(self, instance, validated_data, dictum):
        instance = self.get_instance(instance)

        if len(validated_data.get('number_dictum')) > 5:
            instance.number_dictum = validated_data.get('number_dictum')
            instance.number_receipt_dictum = instance.number_dictum

        if len(str(validated_data.get('date_get_request'))) > 5:
            instance.date_get_request = validated_data.get('date_get_request')

        instance.file_dictum = dictum
        instance.save()
        return instance

    class Meta:
        model = ScholarShip
        fields = ['date_get_request', 'number_dictum', 'file_dictum']


class ReceiptDictumScholarshipSerializer(serializers.ModelSerializer):
    file_receipt_dictum = serializers.FileField(required=True, write_only=True)
    number_receipt_dictum = serializers.CharField(required=True)

    @staticmethod
    def get_instance(pk):
        try:
            return ScholarShip.objects.get(pk=pk)

        except ScholarShip.DoesNotExist:
            raise serializers.ValidationError('NO HAY COINCIDENCIAS')

    def update(self, instance, validated_data, receipt):
        instance = self.get_instance(instance)
        instance.file_receipt_dictum = receipt
        instance.save()
        return instance

    class Meta:
        model = ScholarShip
        fields = ['number_receipt_dictum', 'file_receipt_dictum']


class NotificationScholarshipSerializer(serializers.ModelSerializer):
    file_notification = serializers.FileField(required=True, write_only=True)

    def validate(self, attrs):
        exist = ScholarShip.objects.filter(
            number_notification=attrs.get('number_notification')).exists()

        if exist:
            raise serializers.ValidationError('Ya existe un registro con el código enviado')

        return super().validate(attrs)

    @staticmethod
    def get_instance(pk):
        try:
            return ScholarShip.objects.get(pk=pk)

        except ScholarShip.DoesNotExist:
            raise serializers.ValidationError('NO HAY COINCIDENCIAS')

    def update(self, instance, validated_data, url):
        instance = self.get_instance(instance)

        if len(validated_data.get('number_notification')) > 5:
            instance.number_notification = validated_data.get('number_notification')

        instance.file_notification = url
        instance.save()
        return instance

    class Meta:
        model = ScholarShip
        fields = ['number_notification', 'file_notification']


class ResolutionScholarshipSerializer(serializers.ModelSerializer):
    file_resolution = serializers.FileField(required=True, write_only=True)

    def validate(self, attrs):
        exist = ScholarShip.objects.filter(
            number_resolution=attrs.get('number_resolution')).exists()

        if exist:
            raise serializers.ValidationError('Ya existe un registro con el código enviado')

        return super().validate(attrs)

    @staticmethod
    def get_instance(pk):
        try:
            return ScholarShip.objects.get(pk=pk)

        except ScholarShip.DoesNotExist:
            raise serializers.ValidationError('NO HAY COINCIDENCIAS')

    def update(self, instance, validated_data, url):
        instance = self.get_instance(instance)

        if len(validated_data.get('number_resolution')) > 5:
            instance.number_resolution = validated_data.get('number_resolution')

        instance.file_resolution = url
        instance.save()
        return instance

    class Meta:
        model = ScholarShip
        fields = ['number_resolution', 'file_resolution']


class ReplyScholarshipSerializer(serializers.ModelSerializer):
    file_reply = serializers.FileField(required=True, write_only=True)

    def validate(self, attrs):
        cod = ScholarShip.objects.filter(number_reply=attrs.get('number_reply')).exists()

        if cod:
            raise serializers.ValidationError('Ya existe un registro con el código enviado')

        return super().validate(attrs)

    @staticmethod
    def get_instance(pk):
        try:
            return ScholarShip.objects.get(pk=pk)

        except ScholarShip.DoesNotExist:
            raise serializers.ValidationError('NO HAY COINCIDENCIAS')

    def update(self, instance, validated_data, url):
        instance = self.get_instance(instance)
        instance.number_reply = validated_data.get('number_reply')
        instance.file_reply = url
        instance.save()
        return instance

    class Meta:
        model = ScholarShip
        fields = ['number_reply', 'file_reply']


class DictumBISScholarshipSerializer(serializers.ModelSerializer):
    file_bis = serializers.FileField(required=True, write_only=True)

    def validate(self, attrs):
        cod = ScholarShip.objects.filter(number_bis=attrs.get('number_bis')).exists()

        if cod:
            raise serializers.ValidationError('Ya existe un registro con el código enviado')

        return super().validate(attrs)

    @staticmethod
    def get_instance(pk):
        try:
            return ScholarShip.objects.get(pk=pk)

        except ScholarShip.DoesNotExist:
            raise serializers.ValidationError('NO HAY COINCIDENCIAS')

    def update(self, instance, validated_data, url):
        instance = self.get_instance(instance)

        if len(validated_data.get('number_bis')) > 5:
            instance.number_bis = validated_data.get('number_bis')
            instance.number_receipt_bis = instance.number_bis

        instance.file_bis = url
        instance.save()
        return instance

    class Meta:
        model = ScholarShip
        fields = ['number_bis', 'file_bis']


class ReceiptBisScholarshipSerializer(serializers.ModelSerializer):
    file_receipt_bis = serializers.FileField(required=True, write_only=True)

    @staticmethod
    def get_instance(pk):
        try:
            return ScholarShip.objects.get(pk=pk)

        except ScholarShip.DoesNotExist:
            raise serializers.ValidationError('NO HAY COINCIDENCIAS')

    def update(self, instance, validated_data, url):
        instance = self.get_instance(instance)
        instance.file_receipt_bis = url
        instance.save()
        return instance

    class Meta:
        model = ScholarShip
        fields = ['number_receipt_bis', 'file_receipt_bis']


class FinalizedScholarshipSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=True, write_only=True)

    @staticmethod
    def get_instance(pk):
        try:
            return ScholarShip.objects.get(pk=pk)

        except ScholarShip.DoesNotExist:
            raise serializers.ValidationError('NO HAY COINCIDENCIAS')

    def update(self, instance):
        instance = self.get_instance(instance)
        if instance.finalized:
            instance.finalized = False
        else:
            instance.finalized = True

        instance.save()
        return instance

    class Meta:
        model = ScholarShip
        fields = ['pk']


class ResultScholarshipSerializer(serializers.Serializer):
    scholarship = serializers.IntegerField(required=True)
    result = serializers.IntegerField(required=True)

    def update(self, instance, validated_data):
        if validated_data.get('scholarship') == 1:
            instance.result_promotion = validated_data.get('result')

        elif validated_data.get('scholarship') == 2:
            instance.result_stimulus = validated_data.get('result')

        elif validated_data.get('scholarship') == 3:
            instance.result_trajectory = validated_data.get('result')

        elif validated_data.get('scholarship') == 4:
            instance.result_permanence = validated_data.get('result')

        instance.save()
        return instance


class AdditionalFileSerializer(serializers.ModelSerializer):
    file = serializers.FileField()

    class Meta:
        model = AdditionalFiles
        fields = '__all__'

    def validate(self, attrs):
        number = attrs.get('number_file')
        scholarship = attrs.get('scholarship')

        totals_files = AdditionalFiles.objects.filter(scholarship=scholarship).count()

        if totals_files == 6:
            raise serializers.ValidationError(
                'Solo se permiten 6 archivos adicionales por solicitud')

        cod = AdditionalFiles.objects.filter(
            number_file=number, scholarship=scholarship).exists()

        if cod:
            raise serializers.ValidationError(
                'Ya existe un registro igual asociado a esta soliciutd')

        return super().validate(attrs)

    @staticmethod
    def get_instance(pk):
        try:
            return ScholarShip.objects.get(pk=pk)

        except ScholarShip.DoesNotExist:
            raise serializers.ValidationError('NO HAY COINCIDENCIAS')

    def create(self, validated_data, url):
        scholarship = self.get_instance(int(validated_data.get('scholarship')))
        instance = AdditionalFiles.objects.create(
            scholarship=scholarship, number_file=validated_data.get('number_file'), file=url)
        return instance, scholarship


class AdditionalAllFilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdditionalFiles
        fields = '__all__'
