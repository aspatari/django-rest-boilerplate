#!/usr/bin/env python
import os
import sys

from django.core.management import execute_from_command_line


def set_environment(env_name=None):
    environments = {
        'production' : "config.settings.production",
        'development': "config.settings.development",
        'test'       : "config.settings.test",
    }
    try:
        if env_name:
            env_name = environments[env_name]
        else:
            env_name = environments[os.environ['DJANGO_EXECUTION_ENVIRONMENT']]
    except (KeyError, AttributeError):
        env_name = environments['development']

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", env_name)


if __name__ == "__main__":

    args = sys.argv

    environment = None

    for i, arg in enumerate(args):
        if arg.startswith("--env"):
            key, value = arg.lstrip('-').split('=')
            environment = value
            args.pop(i)

    set_environment(environment)
    execute_from_command_line(args)
