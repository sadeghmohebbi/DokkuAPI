from fastapi import APIRouter, Request, status, Depends
from fastapi.openapi.models import APIKey
from fastapi.responses import JSONResponse
from commands import commands
from router.key import validate_api_key


# Defining our API router
def get_router(app):
    # Create a FastAPI router
    router = APIRouter()

    # Create an application
    @router.post("/proxy/{app_name}/set-ports/{port_mapping}", response_description="Create an application")
    async def create_app(request: Request, app_name: str, port_mapping, api_key: APIKey = Depends(validate_api_key)):
        success, message = commands.proxy_set_ports(app_name, port_mapping)
        content = {"success": success, "message": message}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)

    # We return our router
    return router

