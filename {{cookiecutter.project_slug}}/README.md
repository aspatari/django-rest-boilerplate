# {{cookiecutter.project_name}}
-----

# Environment Variables
## Common

- DJANGO_EXECUTION_ENVIRONMENT
    - Django Environment can be [production, development, test]
- DJANGO_READ_DOT_ENV_FILE
    - If django will read .env file or not

{% if cookiecutter.database_provider  in ["PostgreSQL", "MySQL", "MSSQL"] %}
## Database
- DJANGO_DATABASE_NAME
    - Database Name
    - default='boilerplate'
- DJANGO_DATABASE_USER
    - Database Username
    - default='postgres'
- DJANGO_DATABASE_PASSWORD
    - Database password
- DJANGO_DATABASE_HOST
    - Database host
    - default='localhost'
- DJANGO_DATABASE_PORT
    - Database port
    - default='5432'
- DJANGO_EMAIL_HOST
    - default='localhost'
- DJANGO_USE_DOCKER
    - In case if develop over docker to work debug-tool-bar
- DJANGO_EMAIL_HOST_USER
    - Email user login
- DJANGO_EMAIL_HOST_PASSWORD
    - Email user password

{% endif %}

## Transaction Module
Transactions  contains  3 fields
- user
- valid_until
- action

### User
Is default user object

### Valid Until
Time that transaction will be valid.
Time is set automatic on transaction save

The parameter is taken from setting

#### WorkMode
Valid until can be checked by `is_valid` field
If Transaction is expired it will raise `ExpiredTransaction` exception 


##### Setting Format 
- Format: `{<action_class_name>_<VALID_TIME>} = { key : value }`   
- Key's can be: ['days', 'hours', 'minutes']
- Value is integer

### Action
Actions class is needed to inherit `apps.users.utils.GenericAction`
Actions is a path to class it can be:
- Full path to class
- Class name from `action.py` from the same module


