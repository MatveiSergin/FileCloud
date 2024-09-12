import aiohttp
import fastapi
from fastapi import status
from app.auth import AuthProcess
from app.handlers import http_exception_handler
from api.v1.routers import routers
from utils import get_path_without_domain

app = fastapi.FastAPI(
    title="FileCloud"
)


for router in routers:
    app.include_router(prefix='/files', router=router)

@app.middleware("http")
async def auth(request: fastapi.Request, call_next: fastapi.Response) -> fastapi.Response:
    if '/files/' not in request.url.path:
        return await call_next(request)
    async with aiohttp.ClientSession() as session:
        async with session.post(
                url='http://127.0.0.1:8000/api/v1/auth/check/access',
                headers=request.headers,
                json={'path': get_path_without_domain(request.url.path), 'method': request.method.upper()}
        ) as response:
            response_body = await response.text()
            print(response_body, request.headers)
            auth_response = AuthProcess(response_body).authenticate()
            if auth_response.success:
                request.state.bucket = auth_response.user_id
                return await call_next(request)
            else:
                return http_exception_handler(status.HTTP_401_UNAUTHORIZED, auth_response.detail)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)