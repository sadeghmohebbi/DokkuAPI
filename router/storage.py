from fastapi import APIRouter, Request, status, Depends
from fastapi.openapi.models import APIKey
from fastapi.responses import JSONResponse
from commands import commands
from router.key import validate_api_key


# Defining our API router
def get_router(app):
    # Create a FastAPI router
    router = APIRouter()

    # Mount a Storage
    @router.post("/storage/{app_name}", response_description="Mount a Storage")
    async def create_app(request: Request, app_name: str, api_key: APIKey = Depends(validate_api_key)):
        body_parsed = request.json()
        success, message = commands.storage_mount(app_name=app_name, mount_point_left=body_parsed["mount_point_left"],
                                                  mount_point_right=body_parsed["mount_point_right"])
        content = {"success": success, "message": message}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)

    # We return our router
    return router
