"""
PDF and text file parser.
Extracts raw text from uploaded files.
"""
import re
import logging

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {"pdf", "txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def allowed_file(filename: str) -> bool:
    """Check if the file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(file) -> str:
    """
    Extract text from a PDF file object.
    Uses pypdf (the maintained successor to PyPDF2).
    """
    try:
        from pypdf import PdfReader
    except ImportError:
        # Fallback to PyPDF2 if pypdf not installed yet
        from PyPDF2 import PdfReader

    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    logger.info(f"Extracted {len(text)} characters from PDF ({len(reader.pages)} pages)")
    return text


def extract_text_from_txt(file) -> str:
    """Extract text from a plain text file."""
    content = file.read()
    if isinstance(content, bytes):
        content = content.decode("utf-8", errors="ignore")
    logger.info(f"Read {len(content)} characters from TXT file")
    return content


def extract_text(file) -> str:
    """
    Extract text from any supported file type.
    Auto-detects format from filename.
    """
    filename = getattr(file, "filename", "unknown.pdf")
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if ext == "pdf":
        return extract_text_from_pdf(file)
    elif ext == "txt":
        return extract_text_from_txt(file)
    else:
        raise ValueError(f"Unsupported file type: .{ext}. Allowed: {ALLOWED_EXTENSIONS}")


def extract_topics(text: str) -> list:
    """
    Extract meaningful topic lines from raw text.
    Filters out noise like page numbers, blank lines, etc.
    """
    lines = text.split("\n")
    topics = []

    for line in lines:
        clean = line.strip()

        # Skip junk
        if (
            len(clean) < 8
            or clean.isdigit()
            or re.match(r"^[^a-zA-Z]+$", clean)
            or re.match(r"^page\s*\d+", clean, re.IGNORECASE)
            or len(clean) > 300
        ):
            continue

        topics.append(clean)

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for t in topics:
        normalized = t.lower().strip()
        if normalized not in seen:
            seen.add(normalized)
            unique.append(t)

    logger.info(f"Extracted {len(unique)} unique topics from text")
    return unique