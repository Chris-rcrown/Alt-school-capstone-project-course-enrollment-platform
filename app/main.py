from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api_v1.api import api_router
from app.core.config import settings


def create_app() -> FastAPI:
    cors_origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]

    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_tags=[
            {"name": "Public", "description": "Open endpoints available without a role restriction."},
            {"name": "Auth", "description": "Authentication and account endpoints."},
            {"name": "General", "description": "Authenticated endpoints available to both admins and students."},
            {"name": "Student", "description": "Endpoints reserved for authenticated students."},
            {"name": "Admin", "description": "Endpoints reserved for administrators."},
        ],
    )
    app.include_router(api_router, prefix="/api/v1")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


app = create_app()
