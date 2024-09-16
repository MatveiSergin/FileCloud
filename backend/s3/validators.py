import re
import typing
from app.settings.config import config
from backend.validators import BaseValidator
from exceptions import ValidationError

Path = typing.TypeVar('Path')

class PathValidator(BaseValidator):

    pattern = r'^\/(?:[^\/]+\/)*$'
    error_message = 'Path is not a valid'

    def __init__(self, path: Path):
        self.path = path

    def validate(self) -> Path:
        if self._validate():
            return self.path
        raise ValidationError(self.error_message)

    def _validate(self) -> bool:
        return \
            len(self.path) == 0 or \
            0 < len(self.path) < config.PATH_LENGTH and \
            re.match(self.pattern, self.path)