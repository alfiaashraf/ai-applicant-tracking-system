import logging
import re
import uuid
from pathlib import Path

from fastapi import UploadFile

from app.core.config import Settings, get_settings
from app.core.exceptions import InvalidFileError

logger = logging.getLogger(__name__)


def _extension(filename: str | None) -> str:
    if not filename:
        return ""
    return Path(filename).suffix.lower()


def validate_upload(file: UploadFile, settings: Settings | None = None) -> str:
    settings = settings or get_settings()
    extension = _extension(file.filename)

    if extension not in settings.allowed_extensions:
        raise InvalidFileError(
            f"Unsupported file type '{extension or 'unknown'}'. "
            f"Allowed types: {', '.join(sorted(settings.allowed_extensions))}"
        )

    allowed_content_types = {
        "application/pdf",
        "application/x-pdf",
        "application/octet-stream",
    }
    if file.content_type and file.content_type not in allowed_content_types:
        raise InvalidFileError(
            f"Invalid content type '{file.content_type}'. Expected a PDF upload."
        )

    return extension


async def read_upload_with_limit(
    file: UploadFile,
    settings: Settings | None = None,
) -> bytes:
    settings = settings or get_settings()
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    chunks: list[bytes] = []
    total = 0

    while True:
        chunk = await file.read(1024 * 1024)
        if not chunk:
            break
        total += len(chunk)
        if total > max_bytes:
            raise InvalidFileError(
                f"File exceeds maximum size of {settings.max_upload_size_mb} MB."
            )
        chunks.append(chunk)

    content = b"".join(chunks)
    if not content:
        raise InvalidFileError("Uploaded file is empty.")

    if not content.startswith(b"%PDF"):
        raise InvalidFileError("File does not appear to be a valid PDF.")

    return content


async def save_upload(
    file: UploadFile,
    settings: Settings | None = None,
) -> tuple[Path, str]:
    settings = settings or get_settings()
    extension = validate_upload(file, settings)
    content = await read_upload_with_limit(file, settings)

    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    stored_name = f"{uuid.uuid4().hex}{extension}"
    stored_path = upload_dir / stored_name
    stored_path.write_bytes(content)

    original_name = Path(file.filename or stored_name).name
    logger.info("Saved upload '%s' as '%s'", original_name, stored_name)
    return stored_path, original_name


def safe_remove(path: Path) -> None:
    try:
        path.unlink(missing_ok=True)
    except OSError as exc:
        logger.warning("Failed to remove temporary file %s: %s", path, exc)
