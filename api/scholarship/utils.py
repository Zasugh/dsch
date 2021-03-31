from api.bases.utils import SavedFiles


class ProcessFiles(SavedFiles):

    @classmethod
    def file_save_request(cls, file_data, extension):
        return cls.file_process_name(file_data, 'SOLICITUD', extension, 'REQUESTS')

    @classmethod
    def file_save_dictum(cls, file_data, extension):
        return cls.file_process_name(file_data, 'DICTAMEN', extension, 'DICTUM')

    @classmethod
    def file_save_receipt_dictum(cls, file_data, extension):
        return cls.file_process_name(file_data, 'ACUSE-DICTAMEN', extension, 'RECEIPT_DICTUM')

    @classmethod
    def file_save_notification(cls, file_data, extension):
        parser = extension.split('/')
        name = extension

        if len(parser) > 1:
            name = parser[0]+'-'+parser[1]

        return cls.file_process_name(
            file_data, 'NOTIFICACION-RECEPCION', name, 'RECEIPT_DICTUM')

    @classmethod
    def file_save_resolution(cls, file_data, extension):
        parser = extension.split('/')
        name = extension

        if len(parser) > 1:
            name = parser[0] + '-' + parser[1]

        return cls.file_process_name(file_data, 'RESOLUCION', name, 'RESOLUTION')

    @classmethod
    def file_save_reply(cls, file_data, extension):
        return cls.file_process_name(file_data, 'RESPUESTA-DE-COMISION', extension, 'REPLY')

    @classmethod
    def file_save_bis(cls, file_data, extension):
        return cls.file_process_name(file_data, 'DICTAMEN-BIS', extension, 'BIS')

    @classmethod
    def file_save_receipt_bis(cls, file_data, extension):
        return cls.file_process_name(file_data, 'ACUSE-DICTAMEN-BIS', extension, 'REPLY_BIS')

    @classmethod
    def file_save_additional(cls, file_data, extension):
        parser = extension.split('/')
        name = extension

        if len(parser) > 1:
            name = parser[0] + '-' + parser[1]

        return cls.file_process_name(file_data, 'ADICIONAL', name, 'ADDITIONAL')

    @classmethod
    def delete_file_additional(cls, url):
        return cls.delete_file(url)
