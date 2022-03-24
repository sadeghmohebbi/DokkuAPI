from fastapi import APIRouter, Request, status, Depends
from fastapi.openapi.models import APIKey
from fastapi.responses import JSONResponse
from commands import commands
from router.key import validate_api_key
from pydantic import BaseModel


class StorageMount(BaseModel):
    mount_point_left: str = None
    mount_point_right: str = None


# Defining our API router
def get_router(app):
    # Create a FastAPI router
    router = APIRouter()

    # Mount a Storage
    @router.post("/storage/{app_name}", response_description="Authenticate a git host")
    async def create_app(request: Request, app_name: str, storage_mount: StorageMount,
                         api_key: APIKey = Depends(validate_api_key)):
        success, message = commands.storage_mount(app_name=app_name, mount_point_left=storage_mount.mount_point_left,
                                                  mount_point_right=storage_mount.mount_point_right)
        content = {"success": success, "message": message}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)

    # We return our router
    return router
