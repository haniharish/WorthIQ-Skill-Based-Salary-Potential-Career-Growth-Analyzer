"""
Document text extraction services for PDF and DOCX resume formats.
"""

import os
import logging
from typing import Tuple, List
import pypdf
import docx

logger = logging.getLogger("resumes.parser")

class DocumentParsingError(Exception):
    """Raised when document parsing fails or file is corrupted."""
    pass

class ScannedDocumentWarning(Exception):
    """Raised when a document appears to contain images rather than selectable text."""
    pass

def extract_text_from_pdf(file_path: str) -> Tuple[str, List[str]]:
    """
    Extracts text from a PDF file using pypdf.
    Returns (extracted_text, warnings).
    """
    warnings = []
    text_parts = []
    
    try:
        reader = pypdf.PdfReader(file_path)
        if len(reader.pages) == 0:
            raise DocumentParsingError("PDF file contains no pages.")

        for idx, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text() or ""
                if page_text.strip():
                    text_parts.append(page_text.strip())
            except Exception as e:
                warnings.append(f"Could not extract text from page {idx + 1}: {str(e)}")

        full_text = "\n\n".join(text_parts).strip()

        # Scanned PDF detection
        if len(full_text) < 40:
            warnings.append(
                "Document contains minimal or no selectable text. It may be a scanned or image-based PDF. "
                "For highest extraction accuracy, upload a digitally generated PDF or DOCX."
            )

        return full_text, warnings

    except DocumentParsingError:
        raise
    except Exception as e:
        logger.error(f"Failed to parse PDF {file_path}: {e}")
        raise DocumentParsingError(f"Corrupted or invalid PDF document: {str(e)}")


def extract_text_from_docx(file_path: str) -> Tuple[str, List[str]]:
    """
    Extracts text from a DOCX file using python-docx.
    Iterates over paragraphs and table cells.
    Returns (extracted_text, warnings).
    """
    warnings = []
    text_parts = []

    try:
        doc = docx.Document(file_path)
        
        # Paragraphs
        for p in doc.paragraphs:
            if p.text.strip():
                text_parts.append(p.text.strip())

        # Tables
        for table in doc.tables:
            for row in table.rows:
                row_cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_cells:
                    text_parts.append(" | ".join(row_cells))

        full_text = "\n".join(text_parts).strip()

        if len(full_text) < 40:
            warnings.append("DOCX document appears empty or contains very little text content.")

        return full_text, warnings

    except Exception as e:
        logger.error(f"Failed to parse DOCX {file_path}: {e}")
        raise DocumentParsingError(f"Corrupted or invalid DOCX document: {str(e)}")


def parse_resume_document(file_path: str, file_type: str) -> Tuple[str, List[str]]:
    """
    Dispatches file parsing to appropriate engine based on file_type.
    """
    ext = file_type.lower().replace('.', '')
    if ext == 'pdf':
        return extract_text_from_pdf(file_path)
    elif ext in ['docx', 'doc']:
        return extract_text_from_docx(file_path)
    else:
        raise DocumentParsingError(f"Unsupported file format '.{ext}'. Supported formats: PDF, DOCX.")
