class ExpiredTransaction(Exception):
    """ Exception for showing expired or non valid transaction"""
    pass


def camel_case_split(identifier):
    import re
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0) for m in matches]


class GenericAction:
    name = ''
    description = ''

    def __init__(self, obj, *args, **kwargs) -> None:
        self.obj = obj

        self.settings = {
            "arguments": [*args],
        }

        self.settings.update(kwargs)

    def apply(self):
        raise NotImplementedError

    def execute(self):
        self.pre_execute()
        self.apply()
        self.post_execute()
        self.log_action()

    def pre_execute(self):
        pass

    def post_create(self):
        """Method that is ex after transaction created"""
        pass

    def post_execute(self):
        pass

    def log_action(self):
        pass

    def get_object(self):
        """Return a target object from transaction"""
        return self.obj.user

    def __str__(self) -> str:
        if not self.name:
            self.name = " ".join(camel_case_split(self.__class__.__name__)[:-1])  # if not name put class name s
        return f"{self.name}: {self.description}"
