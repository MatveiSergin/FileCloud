import re
import typing
from app.settings.config import Config
from backend.validators import BaseValidator
from exceptions import ValidationError

Path = typing.TypeVar('Path')

class PathValidator(BaseValidator):

    pattern = r'/^(?:[^\/]+\/)*([^\/]+(?:\.[^\/.]+))?$'
    error_message = 'Path is not a valid'

    def __init__(self, path: Path, bucket_paths: list[Path]):
        self.path = path
        self.bucket_paths = bucket_paths

    def validate(self) -> Path:
        if self._validate():
            return self.path
        raise ValidationError(self.error_message)

    def _validate(self) -> bool:
        print(self.path, self.bucket_paths)
        return \
            len(self.path) == 0 or \
            0 < len(self.path) < Config.PATH_LENGTH and \
            re.match(self.pattern, self.path) and \
            f'/{self.path}/' in self.bucket_paths