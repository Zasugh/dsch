from django.conf import settings

import os


class SavedFiles:
    @staticmethod
    def file_process_name(file_data, name, extension, url_dir, termination='.pdf'):
        extension = str(extension)

        url = settings.MEDIA_ROOT + '/' + url_dir
        url_media = '/media/' + url_dir + '/' + name + '-' + extension + termination
        name_file = name + '-' + extension + termination

        while True:
            try:
                with open(url + '/' + name_file, 'wb') as file:
                    file.write(file_data)
                    file.close()
                    break

            except FileNotFoundError:
                os.mkdir(url)

        return url_media

    @staticmethod
    def delete_file(url):
        parser = url.split('/')
        try:
            os.remove('{}/data/{}/{}'.format(settings.BASE_DIR, parser[2], parser[3]))
        except FileNotFoundError:
            pass
