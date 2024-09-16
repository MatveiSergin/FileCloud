import fastapi
from app.schemas.schemas import File as SchemasFile, AuthRequest, ResponseSchema
from exceptions import ValidationError
from parsers.parsers import ServiceFiles
from s3.s3 import s3_client

router = fastapi.APIRouter(tags=["files"])

@router.get("/")
async def main_page(request: fastapi.Request, path: str = "") -> list[SchemasFile]:
    files_from_s3 = await s3_client.get_folder_contents(path=path, bucket=request.state.bucket)
    files = ServiceFiles().parse_folder(files_from_s3)
    return files


@router.post("/")
async def upload_file(request: fastapi.Request, file: fastapi.UploadFile, path: str = "") -> ResponseSchema:
    try:
        await s3_client.upload_file(file.file, path=path, filename=file.filename, user_bucket=request.state.bucket)
    except ValidationError as e:
        return ResponseSchema(success=False, detail=str(e))
    except Exception as e:
        return ResponseSchema(success=False, detail='Server error')
    else:
        return ResponseSchema(success=True)
