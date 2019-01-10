from django.apps import AppConfig
from django.db.backends.signals import connection_created
from django.db.models.signals import pre_migrate

from . import signals


class CommonConfig(AppConfig):
    name = 'apps.common'
    label = 'common'

    def ready(self):
        # connection_created.connect(signals.database_init_signal)
        # pre_migrate.connect(signals.database_init_signal)
        ...
