from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = "Create default admin user"

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            dest='username',
            default='admin@admin.com',
            help='Admin username',
        )

        parser.add_argument(
            '--password',
            dest='password',
            default='123123123a',
            help='Admin email',
        )

    def handle(self, *args, **options):
        user = get_user_model()
        username = options.get('username')
        password = options.get('password')
        msg = "Default User was created"

        try:
            user.objects.create_superuser(username, password)
        except IntegrityError:
            msg = "User Already exists"

        print(msg)
