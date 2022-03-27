from fastapi import APIRouter, Request, status, Depends
from fastapi.openapi.models import APIKey
from fastapi.responses import JSONResponse
from commands import commands
from router.key import validate_api_key


# Defining our API router
def get_router(app):
    # Create a FastAPI router
    router = APIRouter()

    # Link a database to an app
    @router.post("/databases/links/{plugin_name}/{database_name}/{app_name}",
                 response_description="Link a database to an app")
    async def link_database(request: Request, plugin_name: str, database_name: str, app_name: str,
                            api_key: APIKey = Depends(validate_api_key)):
        success = commands.link_database(plugin_name, database_name, app_name)
        content = {"success": success}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)

    # Unlink a database from an app
    @router.delete("/databases/links/{plugin_name}/{database_name}/{app_name}",
                   response_description="Unlink a database from an app")
    async def unlink_database(request: Request, plugin_name: str, database_name: str, app_name: str,
                              api_key: APIKey = Depends(validate_api_key)):
        success = commands.unlink_database(plugin_name, database_name, app_name)
        content = {"success": success}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)

    # Create a database
    @router.post("/databases/{plugin_name}/{database_name}", response_description="Create a database")
    async def create_database(request: Request, plugin_name: str, database_name: str,
                              api_key: APIKey = Depends(validate_api_key)):
        success = commands.create_database(plugin_name, database_name)
        content = {"success": success}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)

    # Delete a database
    @router.delete("/databases/{plugin_name}/{database_name}", response_description="Delete a database")
    async def delete_database(request: Request, plugin_name: str, database_name: str,
                              api_key: APIKey = Depends(validate_api_key)):
        success = commands.delete_database(plugin_name, database_name)
        content = {"success": success}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)

    # We return our router
    return router
