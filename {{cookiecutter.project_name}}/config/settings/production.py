from .base import *

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
SECRET_KEY = env('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True

# # CACHING
# # ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND" : "django_redis.cache.RedisCache",
        "LOCATION": env.str('DJANGO_CACHE_LOCATION', default="redis://127.0.0.1:6379/1"),
        "OPTIONS" : {
            "CLIENT_CLASS"     : "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        }
    }
}

# region EMAIL
# # ------------------------------------------------------------------------------

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD = env.str("DJANGO_EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = env.str('DJANGO_EMAIL_HOST_USER')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# endregion

# region OPBEAT
# # OPBEAT CONFIGURATION
# # ------------------------------------------------------------------------------
# INSTALLED_APPS += ['opbeat.contrib.django', ]
#
# OPBEAT = {
#     'ORGANIZATION_ID': env('DJANGO_OPBEAT_ORGANIZATION_ID'),
#     'APP_ID'         : env('DJANGO_OPBEAT_APP_ID'),
#     'SECRET_TOKEN'   : env('DJANGO_OPBEAT_SECRET_TOKEN'),
#     'DEBUG': True,
# }
# MIDDLEWARE = ['opbeat.contrib.django.middleware.OpbeatAPMMiddleware', ] + MIDDLEWARE
# endregion
