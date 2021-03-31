from rest_framework import generics, status
from rest_framework.response import Response

from api.bases.views import AccessUserViews

from . import serializers
from .utils import ProcessFiles
from .models import ScholarShip, OptionRequest, AdditionalFiles


class RequestScholarshipView(AccessUserViews, generics.CreateAPIView):
    serializer_class = serializers.RequestScholarshipSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            file = request.FILES['file_request'].read()
            url = ProcessFiles.file_save_request(
                file_data=file, extension=serializer.data.get('number_request'))
            serializer.create(serializer.data, url)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DictumScholarshipView(AccessUserViews, generics.UpdateAPIView):
    serializer_class = serializers.DictumScholarshipSerializer
    queryset = ScholarShip.objects.all()

    @staticmethod
    def get_instance_none(pk):
        instance = ScholarShip.objects.get(pk=pk)
        return instance.number_dictum

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            file_dictum = request.FILES['file_dictum'].read()

            if len(serializer.data.get('number_dictum')) > 5:
                extension = serializer.data.get('number_dictum')

            else:
                extension = self.get_instance_none(self.kwargs['pk'])

            url_dictum = ProcessFiles.file_save_dictum(file_data=file_dictum, extension=extension)
            instance = serializer.update(self.kwargs['pk'], serializer.data, url_dictum)

            return Response(serializers.ScholarshipSerializer(
                instance, context=self.get_serializer_context()).data,
                            status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReceiptDictumScholarshipView(AccessUserViews, generics.UpdateAPIView):
    serializer_class = serializers.ReceiptDictumScholarshipSerializer
    queryset = ScholarShip.objects.all()

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            file_dictum = request.FILES['file_receipt_dictum'].read()

            url_receipt = ProcessFiles.file_save_receipt_dictum(
                file_data=file_dictum,
                extension=serializer.data.get('number_receipt_dictum'))

            instance = serializer.update(self.kwargs['pk'], serializer.data, url_receipt)

            return Response(serializers.ScholarshipSerializer(
                instance, context=self.get_serializer_context()).data,
                            status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationScholarsView(AccessUserViews, generics.UpdateAPIView):
    serializer_class = serializers.NotificationScholarshipSerializer
    queryset = ScholarShip.objects.all()

    @staticmethod
    def get_instance_none(pk):
        instance = ScholarShip.objects.get(pk=pk)
        return instance.number_notification

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            file = request.FILES['file_notification'].read()

            if len(serializer.data.get('number_notification')) > 5:
                extension = serializer.data.get('number_notification')

            else:
                extension = self.get_instance_none(self.kwargs['pk'])

            url = ProcessFiles.file_save_notification(file_data=file, extension=extension)
            instance = serializer.update(self.kwargs['pk'], serializer.data, url)

            return Response(serializers.ScholarshipSerializer(
                instance, context=self.get_serializer_context()).data,
                            status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResolutionScholarsView(AccessUserViews, generics.UpdateAPIView):
    serializer_class = serializers.ResolutionScholarshipSerializer
    queryset = ScholarShip.objects.all()

    @staticmethod
    def get_instance_none(pk):
        instance = ScholarShip.objects.get(pk=pk)
        return instance.number_resolution

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            file = request.FILES['file_resolution'].read()

            if len(serializer.data.get('number_resolution')) > 5:
                extension = serializer.data.get('number_resolution')

            else:
                extension = self.get_instance_none(self.kwargs['pk'])

            url = ProcessFiles.file_save_resolution(file_data=file, extension=extension)
            instance = serializer.update(self.kwargs['pk'], serializer.data, url)

            return Response(serializers.ScholarshipSerializer(
                instance, context=self.get_serializer_context()).data,
                            status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReplyScholarsView(AccessUserViews, generics.UpdateAPIView):
    serializer_class = serializers.ReplyScholarshipSerializer
    queryset = ScholarShip.objects.all()

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            file = request.FILES['file_reply'].read()

            url = ProcessFiles.file_save_reply(
                file_data=file, extension=serializer.data.get('number_reply'))

            instance = serializer.update(self.kwargs['pk'], serializer.data, url)

            return Response(serializers.ScholarshipSerializer(
                instance, context=self.get_serializer_context()).data,
                            status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BISScholarsView(AccessUserViews, generics.UpdateAPIView):
    serializer_class = serializers.DictumBISScholarshipSerializer
    queryset = ScholarShip.objects.all()

    @staticmethod
    def get_instance_none(pk):
        instance = ScholarShip.objects.get(pk=pk)
        return instance.number_bis

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            file = request.FILES['file_bis'].read()

            if len(serializer.data.get('number_bis')) > 5:
                extension = serializer.data.get('number_bis')

            else:
                extension = self.get_instance_none(self.kwargs['pk'])

            url = ProcessFiles.file_save_bis(file_data=file, extension=extension)
            instance = serializer.update(self.kwargs['pk'], serializer.data, url)
            return Response(serializers.ScholarshipSerializer(
                instance, context=self.get_serializer_context()).data,
                            status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReceiptBisScholarsView(AccessUserViews, generics.UpdateAPIView):
    serializer_class = serializers.ReceiptBisScholarshipSerializer
    queryset = ScholarShip.objects.all()

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            file = request.FILES['file_receipt_bis'].read()

            url = ProcessFiles.file_save_receipt_bis(
                file_data=file, extension=serializer.data.get('number_receipt_bis'))

            instance = serializer.update(self.kwargs['pk'], serializer.data, url)

            return Response(serializers.ScholarshipSerializer(
                instance, context=self.get_serializer_context()).data,
                            status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestScholarshipListYear(AccessUserViews, generics.ListAPIView):
    serializer_class = serializers.ScholarshipSerializer

    def get_queryset(self):
        if self.kwargs['op'] == 1:
            return ScholarShip.objects.filter(
                year=self.kwargs['year'], promotion=True, is_active=True)

        elif self.kwargs['op'] == 2:
            return ScholarShip.objects.filter(
                year=self.kwargs['year'], stimulus=True, is_active=True)

        elif self.kwargs['op'] == 3:
            return ScholarShip.objects.filter(
                year=self.kwargs['year'], trajectory=True, is_active=True)

        elif self.kwargs['op'] == 4:
            return ScholarShip.objects.filter(
                year=self.kwargs['year'], permanence=True, is_active=True)

        elif self.kwargs['op'] == 5:
            return ScholarShip.objects.filter(
                year=self.kwargs['year'], is_active=True)


class RequestScholarshipListNumber(AccessUserViews, generics.ListAPIView):
    serializer_class = serializers.ScholarshipSerializer

    def get_queryset(self):
        if self.kwargs['op'] == 1:
            return ScholarShip.objects.filter(
                user__number=self.kwargs['number'], promotion=True, is_active=True)

        elif self.kwargs['op'] == 2:
            return ScholarShip.objects.filter(
                user__number=self.kwargs['number'], stimulus=True, is_active=True)

        elif self.kwargs['op'] == 3:
            return ScholarShip.objects.filter(
                user__number=self.kwargs['number'], trajectory=True, is_active=True)

        elif self.kwargs['op'] == 4:
            return ScholarShip.objects.filter(
                user__number=self.kwargs['number'], permanence=True, is_active=True)

        elif self.kwargs['op'] == 5:
            return ScholarShip.objects.filter(
                user__number=self.kwargs['number'], is_active=True)


class RequestScholarshipRetrieve(AccessUserViews, generics.RetrieveAPIView):
    serializer_class = serializers.ScholarshipSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ScholarShip.objects.none()

        return ScholarShip.objects.get(pk=self.kwargs['pk'])

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_queryset()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        except ScholarShip.DoesNotExist:
            return Response({'detail': 'No hay coincidencias'},
                            status=status.HTTP_404_NOT_FOUND)


class OptionRequestList(AccessUserViews, generics.ListAPIView):
    serializer_class = serializers.OptionRequestSerializer

    def get_queryset(self):
        return OptionRequest.objects.all()


class FinalizedScholarshipView(AccessUserViews, generics.UpdateAPIView):
    serializer_class = serializers.FinalizedScholarshipSerializer
    queryset = ScholarShip.objects.all()

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.kwargs)

        if serializer.is_valid():
            instance = serializer.update(self.kwargs['pk'])
            return Response(serializers.ScholarshipSerializer(
                instance, context=self.get_serializer_context()).data,
                            status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteScholarshipView(AccessUserViews, generics.DestroyAPIView):
    serializer_class = None
    queryset = ScholarShip.objects.all()

    def get_object(self):
        try:
            return ScholarShip.objects.get(pk=self.kwargs['pk'])

        except ScholarShip.DoesNotExist:
            return None

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        return instance

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance is not None:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_404_NOT_FOUND)


class ResultScholarshipView(AccessUserViews, generics.UpdateAPIView):
    serializer_class = serializers.ResultScholarshipSerializer
    queryset = ScholarShip.objects.all()

    def get_object(self):
        try:
            return ScholarShip.objects.get(pk=self.kwargs['pk'])

        except ScholarShip.DoesNotExist:
            return None

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            instance = self.get_object()

            if instance is not None:
                obj = serializer.update(instance, serializer.data)
                context = serializers.ScholarshipSerializer(
                    obj, context=self.get_serializer_context())
                return Response(context.data, status=status.HTTP_200_OK)

            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_202_ACCEPTED)


class AdditionalFilesView(AccessUserViews, generics.CreateAPIView):
    serializer_class = serializers.AdditionalFileSerializer
    queryset = AdditionalFiles.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            file = request.FILES['file'].read()
            url = ProcessFiles.file_save_additional(
                file_data=file, extension=serializer.data.get('number_file'))
            instance, scholarship = serializer.create(serializer.data, url)

            serializer = serializers.AdditionalAllFilesSerializer(
                scholarship.files.all(), many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdditionalFilesList(AccessUserViews, generics.ListAPIView):
    serializer_class = serializers.AdditionalAllFilesSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return AdditionalFiles.objects.none()

        return AdditionalFiles.objects.filter(scholarship=self.kwargs['pk'])

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if len(queryset) > 0:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status.HTTP_200_OK)

        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteAdditionalFileView(AccessUserViews, generics.DestroyAPIView):
    serializer_class = None
    queryset = AdditionalFiles.objects.all()

    def get_object(self):
        try:
            return AdditionalFiles.objects.get(pk=self.kwargs['pk'])

        except AdditionalFiles.DoesNotExist:
            return None

    def perform_destroy(self, instance):
        ProcessFiles.delete_file_additional(instance.file)
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance is not None:
            files = AdditionalFiles.objects.filter(scholarship=instance.scholarship)
            self.perform_destroy(instance)
            if len(files) > 0:
                serializer = serializers.AdditionalAllFilesSerializer(files, many=True)
                return Response(serializer.data, status.HTTP_200_OK)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
