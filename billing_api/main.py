from contextlib import asynccontextmanager
from json import JSONEncoder
from uuid import UUID

import uvicorn
from api.v1 import billing, content
from core.config import settings
from db.postgres import engine
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    swagger_ui_parameters={"syntaxHighlight": False},
    lifespan=lifespan,
)

add_pagination(app)


def custom_openapi():
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title=settings.project_name,
            version="1.0.0",
            openapi_version="3.0.0",
            description="",
            routes=app.routes,
            tags="",
            servers="",
        )
        for _, method_item in app.openapi_schema.get("paths").items():
            for _, param in method_item.items():
                responses = param.get("responses")
                if "422" in responses:
                    del responses["422"]
                if "200" in responses:
                    del responses["200"]
    return app.openapi_schema


app.openapi = custom_openapi

old_default = JSONEncoder.default


def new_default(self, obj):
    if isinstance(obj, UUID):
        return str(obj)
    return old_default(self, obj)


JSONEncoder.default = new_default


@app.on_event("startup")
async def startup_event():
    # await get_rabbitmq()

    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    pass


@app.on_event("shutdown")
async def shutdown_event():
    # await close_rabbitmq()
    # await db.close()
    pass


app.include_router(billing.router, prefix="/api/v1/billing", tags=["billing"])
app.include_router(content.router, prefix="/api/v1/content", tags=["content"])

if __name__ == "__main__":
    uvicorn.run(
        app,  # type: ignore
        host="0.0.0.0",
        port=8000,
    )
