# Imports
from fastapi import FastAPI
from router.meta import get_router as meta_router
from router.apps import get_router as app_router
from router.plugins import get_router as plugin_router
from router.databases import get_router as database_router
from router.domains import get_router as domain_router
from router.config import get_router as config_router
from router.git import get_router as git_router
from router.proxy import get_router as proxy_router
from router.storage import get_router as storage_router

# Create the FastAPP app
app = FastAPI()

origins = [
    "*",
]


# Startup Event
@app.on_event("startup")
async def startup_db_client():
    pass


# Shutdown Event
@app.on_event("shutdown")
async def shutdown_db_client():
    pass


# Include our API router
app.include_router(meta_router(app), tags=["Api"], prefix="/api")
app.include_router(app_router(app), tags=["Apps"], prefix="/api")
app.include_router(plugin_router(app), tags=["Plugins"], prefix="/api")
app.include_router(database_router(app), tags=["Databases"], prefix="/api")
app.include_router(domain_router(app), tags=["Domains"], prefix="/api")
app.include_router(config_router(app), tags=["Config"], prefix="/api")
app.include_router(git_router(app), tags=["Git"], prefix="/api")
app.include_router(proxy_router(app), tags=["Proxy"], prefix="/api")
app.include_router(storage_router(app), tags=["Storage"], prefix="/api")

