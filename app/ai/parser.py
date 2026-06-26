from pathlib import Path
from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    return text


def load_all_resumes(folder_path: str):

    resumes = {}

    for pdf in Path(folder_path).glob("*.pdf"):
        resumes[pdf.name] = extract_text_from_pdf(pdf)

    return resumes