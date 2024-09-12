from abc import ABC, abstractmethod
import aiofiles

class AbstractFile(ABC):

    def __init__(self, file_name: str, content: bytes):
        self.file_name = file_name
        self.content = content

    @abstractmethod
    async def make_file_descriptor(self):
        pass



class File(AbstractFile):

    async def make_file_descriptor(self):
        async with aiofiles.open(self.file_name, mode="wb") as file:
            await file.write(self.content)
            return file
