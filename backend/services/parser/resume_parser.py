from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree
from zipfile import BadZipFile, ZipFile

import fitz


@dataclass(frozen=True)
class ParseResult:
    """Outcome of parsing a single resume file.

    `clean` is True only when the format-specific parser (PDF/DOCX) ran
    without error. Anything that hit the raw-byte fallback is `clean=False`,
    because that path can produce garbled or partial text — downstream
    confidence scoring needs to know this happened, not just receive text.
    """

    text: str
    clean: bool
    method: str  # "pdf" | "docx" | "plaintext" | "fallback"


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


def parse_resume_with_metadata(path) -> ParseResult:
    """Parse a resume and report how reliable the extraction was.

    This is the source of truth for parse quality. `parse_resume()` below
    wraps this for callers that only want the text (e.g. embedding), but
    anything that needs to judge evidence reliability (confidence engine)
    should call this directly.
    """
    resume_path = Path(path)
    extension = resume_path.suffix.lower()

    try:
        if extension == ".pdf":
            return ParseResult(text=_parse_pdf(resume_path).strip(), clean=True, method="pdf")

        if extension == ".docx":
            return ParseResult(text=_parse_docx(resume_path).strip(), clean=True, method="docx")

        text = resume_path.read_text(encoding="utf-8", errors="ignore").strip()
        return ParseResult(text=text, clean=True, method="plaintext")

    except (RuntimeError, ValueError, BadZipFile, KeyError, ElementTree.ParseError):
        # Format-specific parsing failed (corrupt PDF, malformed DOCX zip,
        # unexpected XML shape). Fall back to raw decode so we still have
        # *something* to embed, but flag it as unclean — this text may be
        # missing structure, contain binary noise, or be incomplete.
        text = _read_text_fallback(resume_path).strip()
        return ParseResult(text=text, clean=False, method="fallback")


def parse_resume(path) -> str:
    """Convenience wrapper for callers that only need resume text."""
    return parse_resume_with_metadata(path).text