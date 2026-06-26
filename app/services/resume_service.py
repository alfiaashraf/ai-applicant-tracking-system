import asyncio
import logging
from pathlib import Path

from pypdf.errors import PdfReadError

from app.ai.parser import extract_text_from_pdf
from app.ai.preprocess import clean_text
from app.ai.skill_extractor import extract_skills
from app.core.exceptions import EmptyDocumentError, PDFParseError
from app.schemas.resume import ResumeAnalyzeResponse

logger = logging.getLogger(__name__)


def extract_resume_text(pdf_path: Path) -> str:
    try:
        text = extract_text_from_pdf(str(pdf_path))
    except PdfReadError as exc:
        raise PDFParseError(f"Unable to read PDF: {exc}") from exc
    except OSError as exc:
        raise PDFParseError(f"Unable to open PDF: {exc}") from exc

    if not text.strip():
        raise EmptyDocumentError("No text could be extracted from the PDF.")

    return text


def _analyze_resume_sync(pdf_path: Path, filename: str) -> ResumeAnalyzeResponse:
    logger.info("Analyzing resume '%s'", filename)
    text = extract_resume_text(pdf_path)
    cleaned = clean_text(text)
    skills = extract_skills(text)

    return ResumeAnalyzeResponse(
        filename=filename,
        cleaned_text=cleaned,
        skills=skills,
    )


async def analyze_resume(pdf_path: Path, filename: str) -> ResumeAnalyzeResponse:
    return await asyncio.to_thread(_analyze_resume_sync, pdf_path, filename)
