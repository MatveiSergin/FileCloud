from app.api.v1.endpoints.files import router as files_router
from app.api.v1.endpoints.auth import router as auth_router


routers = [
    files_router,
    auth_router
]