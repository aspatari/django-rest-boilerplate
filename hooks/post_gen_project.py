import os
import shutil

# Get the root project directory
PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)
USE_CELERY = '{{cookiecutter.use_celery}}'


def remove_task_app(project_directory):
    """Removes the taskapp if celery isn't going to be used"""
    # Determine the local_setting_file_location
    task_app_location = os.path.join(
        project_directory,
        'apps/taskapp'
    )
    shutil.rmtree(task_app_location)


if USE_CELERY == 'n':
    remove_task_app(PROJECT_DIRECTORY)