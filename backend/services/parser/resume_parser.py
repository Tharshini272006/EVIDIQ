from pathlib import Path
from xml.etree import ElementTree
from zipfile import BadZipFile, ZipFile

import fitz


def _read_text_fallback(path: Path) -> str:
    return path.read_bytes().decode("utf-8", errors="ignore")


def _parse_pdf(path: Path) -> str:
    text = ""

    with fitz.open(path) as doc:
        for page in doc:
            text += page.get_text()

    return text


def _parse_docx(path: Path) -> str:
    with ZipFile(path) as docx:
        xml = docx.read("word/document.xml")

    root = ElementTree.fromstring(xml)
    parts = [node.text for node in root.iter() if node.text]
    return " ".join(parts)


def parse_resume(path):
    resume_path = Path(path)
    extension = resume_path.suffix.lower()

    try:
        if extension == ".pdf":
            return _parse_pdf(resume_path).strip()

        if extension == ".docx":
            return _parse_docx(resume_path).strip()

        return resume_path.read_text(encoding="utf-8", errors="ignore").strip()
    except (RuntimeError, ValueError, BadZipFile, KeyError, ElementTree.ParseError):
        return _read_text_fallback(resume_path).strip()
