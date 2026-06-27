from app.database import Base, engine
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.exceptions import (
    AppError,
    EmptyDocumentError,
    InvalidFileError,
    JobNotFoundError,
    PDFParseError,
)
from app.core.logging_config import setup_logging
from app.routers.health import router as health_router
from app.routers.jobs import router as jobs_router
from app.routers.ranking import router as ranking_router
from app.routers.resume import router as resume_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    settings = get_settings()
    logger.info("Starting %s v%s", settings.app_name, settings.app_version)
    yield
    logger.info("Shutting down %s", settings.app_name)


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "AI-powered applicant tracking API for recruiters. "
            "Manage job postings, analyze resumes, and rank candidates "
            "using TF-IDF and semantic similarity."
        ),
        lifespan=lifespan,
    )
    Base.metadata.create_all(bind=engine)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(InvalidFileError)
    async def invalid_file_handler(
        request: Request,
        exc: InvalidFileError,
    ) -> JSONResponse:
        logger.warning("Invalid file upload on %s: %s", request.url.path, exc.message)
        return JSONResponse(status_code=400, content={"detail": exc.message})

    @app.exception_handler(PDFParseError)
    async def pdf_parse_handler(
        request: Request,
        exc: PDFParseError,
    ) -> JSONResponse:
        logger.warning("PDF parse error on %s: %s", request.url.path, exc.message)
        return JSONResponse(status_code=422, content={"detail": exc.message})

    @app.exception_handler(EmptyDocumentError)
    async def empty_document_handler(
        request: Request,
        exc: EmptyDocumentError,
    ) -> JSONResponse:
        logger.warning("Empty document on %s: %s", request.url.path, exc.message)
        return JSONResponse(status_code=422, content={"detail": exc.message})

    @app.exception_handler(JobNotFoundError)
    async def job_not_found_handler(
        request: Request,
        exc: JobNotFoundError,
    ) -> JSONResponse:
        logger.warning("Job not found on %s: %s", request.url.path, exc.message)
        return JSONResponse(status_code=404, content={"detail": exc.message})

    @app.exception_handler(AppError)
    async def app_error_handler(
        request: Request,
        exc: AppError,
    ) -> JSONResponse:
        logger.error("Application error on %s: %s", request.url.path, exc.message)
        return JSONResponse(status_code=500, content={"detail": exc.message})

    app.include_router(health_router)
    app.include_router(jobs_router)
    app.include_router(resume_router)
    app.include_router(ranking_router)

    return app


app = create_app()
