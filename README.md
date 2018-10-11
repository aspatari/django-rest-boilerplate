# DJANGO REST BOILERPLATE

## Install
```
$ cookiecutter https://github.com/aspatari/django-rest-boilerplate
```
```
# pip install black
# pip install tmuxp
```
```
$ cd `project_dir`
$ echo 'DJANGO_DATABASE_PASSWORD=`db_pass`' > .env
$ tmuxp load .tmuxp.yaml
```
######MySQL8
```
if docker:
    $ docker exec -it CONTAINER_ID /bin/bash
$ mysql --user=root --password
ALTER USER 'username' IDENTIFIED WITH mysql_native_password BY 'password';
[source](https://stackoverflow.com/questions/49194719/authentication-plugin-caching-sha2-password-cannot-be-loaded)
```