from contextlib import asynccontextmanager
from tempfile import SpooledTemporaryFile

import fastapi
from aiobotocore.session import get_session
from app.settings.settings import settings
from exceptions import ArgumentError, ValidationError
from s3.file import File, AbstractFile
from s3.validators import PathValidator, Path
from utils import get_unique_files, has_substring_in_strings
from validators import BaseValidator


class S3Client:
    def __init__(self,
                 access_key: str,
                 secret_key: str,
                 bucket_name: str,
                 endpoint_url: str,
                 file_type: AbstractFile = File,
                 path_validator: BaseValidator = PathValidator
                 ):

        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name
        self.endpoint_url = endpoint_url
        self._file_type = file_type
        self._path_validator = path_validator

        self.config = {
            'endpoint_url': self.endpoint_url,
            'aws_access_key_id': self.access_key,
            'aws_secret_access_key': self.secret_key
        }

        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(self,
                          file: SpooledTemporaryFile,
                          user_bucket: str,
                          filename: str,
                          path: str,
                          ) -> None:

        self._path_validator(
            path
            ).validate()

        absolute_path = f'{user_bucket}{path}{filename}'
        async with self.get_client() as client:
            print(self.bucket_name, absolute_path, file)
            await client.put_object(Bucket=self.bucket_name, Key=absolute_path, Body=file)

    async def get_folder_contents(self, path: Path, user_bucket: str) -> list[dict]:
        path = f'{user_bucket}{path}'

        user_paths = await self._get_user_paths(user_bucket)
        if not has_substring_in_strings(path, user_paths):
            return []

        try:
            path = self._path_validator(path).validate()
        except ValidationError as e:
            return []

        async with self.get_client() as client:
            paginator = client.get_paginator('list_objects_v2')
            files = []
            async for result in paginator.paginate(Bucket=self.bucket_name, Prefix=path):
                for content in result.get('Contents', []):
                    print(content) #todo remove
                    content = self._processing_content(content, path)
                    files.append(content)
            return get_unique_files(files)

    async def _get_user_paths(self, user_bucket: str) -> list[Path]:
        async with self.get_client() as client:
            paginator = client.get_paginator('list_objects')
            paths = []
            async for result in paginator.paginate(Bucket=self.bucket_name, Prefix=user_bucket):
                for content in result.get('Contents', []):
                    paths.append(content['Key'])
            return paths

    def _processing_content(self, content: dict, path: Path) -> dict:
        if len(path) != 0:
            postfix = content['Key'][len(path):]
        else:
            postfix = content['Key']
        if "/" in postfix:
            content['Key'] = postfix[:postfix.index("/")]
            content['Type'] = 'folder'
        else:
            content['Key'] = postfix
            content['Type'] = 'file'
        return content

    async def get_file(self, path: Path):
        async with self.get_client() as client:
            object = await client.get_object(Bucket=self.bucket_name, Key=path)
            async with object["Body"] as stream:
                content = await stream.read()
                return self._file_type(path, content)





s3_client = S3Client(
    access_key=settings.ACCESS_KEY,
    secret_key=settings.SECRET_KEY,
    bucket_name=settings.BUCKET_NAME,
    endpoint_url=settings.ENDPOINT_URL
)




