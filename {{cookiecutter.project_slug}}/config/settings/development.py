import os
import socket

from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
CORS_ORIGIN_ALLOW_ALL = True
# DJANGO EXTENSIONS
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['django_extensions', ]

# DEBUG TOOLBAR
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['debug_toolbar', ]
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', ]
# tricks to have debug toolbar when developing with docker
if os.environ.get('DJANGO_USE_DOCKER') == 'yes':
    ip = socket.gethostbyname(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + '1']

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS'       : [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

# Mail settings
# ------------------------------------------------------------------------------
EMAIL_PORT = 1025
EMAIL_HOST = env('DJANGO_EMAIL_HOST', default='localhost')

# # CACHING
# # ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND" : "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS" : {
            "CLIENT_CLASS"     : "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        }
    }
}

# # TESTING
# # ------------------------------------------------------------------------------
# TEST_RUNNER = 'django.test.runner.DiscoverRunner'

{% if cookiecutter.use_celery == "y" %}

# CELERY
# ------------------------------------------------------------------------------
# In development, all tasks will be executed locally by blocking until the task returns
CELERY_ALWAYS_EAGER = True
# END CELERY
{% endif %}

# region SILK
# SILK
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['silk']  # https://github.com/jazzband/django-silk

MIDDLEWARE.insert(0, "silk.middleware.SilkyMiddleware")
SILKY_AUTHENTICATION = True  # User must login
SILKY_AUTHORISATION = True  # User must have permissions
SILKY_PERMISSIONS = lambda user: user.is_staff
# endregion


POST_REGISTRATION_CONFIRM_ACTION_VALID_TIME = {"days": 30}
RESET_PASSWORD_ACTION_VALID_TIME = {"days": 30}
