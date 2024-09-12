

class BaseException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        return f'{self.__class__} has been raised. {self.message}'


class ArgumentError(BaseException):
    pass


class ValidationError(BaseException):
    pass

