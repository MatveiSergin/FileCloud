import fastapi
from app.schemas.schemas import File as SchemasFile, AuthRequest
from parsers.parsers import ServiceFiles
from s3.s3 import s3_client

router = fastapi.APIRouter(tags=["files"])

@router.get("/")
async def main_page(request: fastapi.Request, path: str = "") -> list[SchemasFile]:
    files_from_s3 = await s3_client.get_folder_contents(path=path, bucket=request.state.bucket)
    files = ServiceFiles().parse_folder(files_from_s3)
    return files


@router.post("/")
async def upload_file(file: fastapi.UploadFile, path: str = "") -> AuthRequest:
    try:
        await s3_client.upload_file(file.file, path)
    except Exception as e:
        print(e)
        return AuthRequest(success=False)
    else:
        return AuthRequest(success=True)
