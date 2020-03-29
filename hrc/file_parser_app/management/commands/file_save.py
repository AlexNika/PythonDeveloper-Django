import os
import tempfile

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.utils import timezone

from file_parser_app.models import File
from hrc.settings import MEDIA_ROOT


class Command(BaseCommand):
    help = 'Save local file(s) for further parsing'

    def add_arguments(self, parser):
        parser.add_argument('upload_files', nargs='+', type=str)

    def handle(self, *args, **options):
        # Заполенние мадели File
        # + Копирование файла модели File в /media/upload/
        upload_file = options['upload_files'][0]
        upload_file_description = ' '.join(options['upload_files'][1:])
        upload_file_name = os.path.basename(upload_file)
        if os.path.exists(upload_file):
            try:
                file = File.objects.get(file_name=upload_file_name)
                file.file_timestamp = timezone.now()
                file.save()
            except ObjectDoesNotExist:
                file = File(file_name=upload_file_name,
                            file_description=upload_file_description,
                            file_timestamp=timezone.now())
                file.save()
            finally:
                temp_file = tempfile.NamedTemporaryFile(dir=os.path.join(MEDIA_ROOT, 'uploads'), delete=False)
                f = open(upload_file, 'rb')
                temp_file.write(f.read())
                temp_file.close()
                existing_file = os.path.join(MEDIA_ROOT, 'uploads', upload_file_name)
                try:
                    os.rename(temp_file.name, existing_file)
                except FileExistsError:
                    os.remove(existing_file)
                    os.rename(temp_file.name, existing_file)
                self.stdout.write(f'Successfully upload file {upload_file_name}')
        else:
            self.stdout.write(f'Alert! File {upload_file} not available.')
