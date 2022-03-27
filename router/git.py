from fastapi import APIRouter, Request, status, Depends
from fastapi.openapi.models import APIKey
from fastapi.responses import JSONResponse
from commands import commands
from router.key import validate_api_key


# Defining our API router
def get_router(app):
    # Create a FastAPI router
    router = APIRouter()

    # Authenticate a git host
    @router.post("/git/{host}/auth", response_description="Authenticate a git host")
    async def create_app(request: Request, host: str, api_key: APIKey = Depends(validate_api_key)):
        body_parsed = await request.json()
        success = commands.git_auth(host=host, username=body_parsed["username"],
                                             password=body_parsed["password"])
        content = {"success": success}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)

    # Updates an app's git repository with a given docker image
    @router.post("/git/{app_name}/from-image", response_description="Updates an app's git repository with a given docker image")
    async def create_app(request: Request, app_name: str, api_key: APIKey = Depends(validate_api_key)):
        body_parsed = await request.json()
        success = commands.git_from_image(app_name=app_name, docker_image=body_parsed["docker_image"])
        content = {"success": success}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)

    # We return our router
    return router
