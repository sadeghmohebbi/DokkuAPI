from fastapi import APIRouter, Request, status, Depends
from fastapi.openapi.models import APIKey
from fastapi.responses import JSONResponse
from commands import commands
from router.key import validate_api_key
from pydantic import BaseModel


class UserInfo(BaseModel):
    username: str = None
    password: str = None


class DockerImage(BaseModel):
    name: str = None


# Defining our API router
def get_router(app):
    # Create a FastAPI router
    router = APIRouter()

    # Authenticate a git host
    @router.post("/git/{host}/auth", response_description="Authenticate a git host")
    async def create_app(request: Request, host: str, user_info: UserInfo, api_key: APIKey = Depends(validate_api_key)):
        success, message = commands.git_auth(host=host, username=user_info.username, password=user_info.password)
        content = {"success": success, "message": message}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)

    # Updates an app's git repository with a given docker image
    @router.post("/git/{app_name}/from-image/{docker_image}",
                 response_description="Updates an app's git repository with a given docker image")
    async def create_app(request: Request, app_name: str, docker_image: DockerImage,
                         api_key: APIKey = Depends(validate_api_key)):
        success, message = commands.git_from_image(app_name=app_name, docker_image=docker_image.name)
        content = {"success": success, "message": message}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)

    # We return our router
    return router
