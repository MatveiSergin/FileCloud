import asyncio
import aiofiles
from backend.s3.s3 import S3Client

client = S3Client(
    access_key="1Q9T0TO2SNVUT6N8JEG4",
    secret_key="rEkM82HpV9OdlwDiRDeCp3T2AGCIwHn6llGwGhri",
    bucket_name="095258df-babbfe39-b31f-47a5-aaa9-476ba3e3d4f6",
    endpoint_url="https://s3.timeweb.cloud"
)

async def main():
    async with aiofiles.open("file.txt", mode="rb") as file:
        content = await file.read()
        print(content)
        await client.upload_file(file=content, path="folder/inner_folder/file.txt")
if __name__ == "__main__":
    asyncio.run(main())