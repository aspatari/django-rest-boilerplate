from django.core.management import CommandError
from django.core.management.templates import TemplateCommand
from os import path
import os


class Command(TemplateCommand):
    help = (
        "Creates a Django app directory structure for the given app name in "
        "the current directory or optionally in the given directory."
    )
    missing_args_message = "You must provide an application name."

    def handle(self, **options):
        options['template'] = 'https://github.com/aspatari/django-rest-framework-app-tempalte/archive/master.zip'
        app_name = options.pop("name")
        top_dir = path.join(os.getcwd(), "apps", app_name)
        try:
            os.makedirs(top_dir)
        except FileExistsError:
            raise CommandError("'%s' already exists" % top_dir)
        except OSError as e:
            raise CommandError(e)

        super().handle("app", app_name, top_dir, **options)
    # pm startapp events apps/events --template https://github.com/aspatari/django-rest-framework-app-tempalte/archive/master.zip
