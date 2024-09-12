from abc import ABC, abstractmethod

class AbstractParser(ABC):
    @abstractmethod
    def parse(self, config: dict) -> dict:
        ...

    @abstractmethod
    def _parse(self, **kwargs) -> dict:
        ...
class FileParser:

    dict_naming = {
        'has_name': 'Key',
        'has_last_modified': 'LastModified',
        'has_size': 'Size',
        'has_owner': 'Owner',
        'has_type': 'Type',
    }

    def __init__(self, config: dict):
        self.config = config

    def parse(self,
              has_name: bool = True,
              has_last_modified: bool = True,
              has_size: bool = True,
              has_type: bool = True,
              has_owner: bool = False,
              ) -> dict:
        return self._parse(
            has_name=has_name,
            has_last_modified=has_last_modified,
            has_size=has_size,
            has_owner=has_owner,
            has_type=has_type,
        )

    def _parse(self, **kwargs):
        parsing_config = {}
        for key, value in kwargs.items():
            arg = self.dict_naming[key]
            if value:
                parsing_config["".join(key.split("_")[1:])] = self.config.get(arg, None)

        return parsing_config

class ServiceFiles:
    def __init__(self, parser: AbstractParser = FileParser):
        self.parser = parser

    def parse_file(self, config: dict) -> dict:
        return FileParser(config).parse(self.parser)

    def parse_folder(self, config: list[dict]) -> list[dict]:
        folder_data = []
        for config in config:
            folder_data += [self.parse_file(config)]
        return folder_data