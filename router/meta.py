from fastapi import APIRouter, Request, status, Depends
from fastapi.responses import JSONResponse
from config import settings
from commands import commands
from router.key import validate_api_key
from fastapi.openapi.models import APIKey

# Defining our API router
def get_router(app):
    # Create a FastAPI router
    router = APIRouter()

    # We define a root path for our API with metadata
    @router.get("/", response_description="API Metadata")
    async def metadata(request: Request, api_key: APIKey = Depends(validate_api_key)):
        result = {
            "api": settings.API_NAME,
            "healthy": commands.list_apps(),
            "version": settings.API_VERSION_NUMBER,
            "author": "Sadegh Mohebbi",
            "company": "PingBeen",
            "website": "https://pingbeen.com",
            "email": "mohebbi.sadegh@gmail.com",
        }
        return JSONResponse(status_code=status.HTTP_200_OK, content=result)

    # We return our router
    return router

