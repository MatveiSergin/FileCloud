import fastapi
from fastapi.responses import JSONResponse


def http_exception_handler(status: fastapi.status, detail: str) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        content={
            'detail': detail
        })