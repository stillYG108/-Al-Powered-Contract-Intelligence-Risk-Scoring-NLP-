"""
ingestion/pdf_extractor.py
==========================
Text extractor for DIGITAL PDF files (text layer is selectable/copyable).

PURPOSE
-------
Extracts text from PDFs where a real text layer exists — no OCR needed.
Uses pdfminer.six because it gives character-level positioning data,
which is useful for later Phase-3 highlighting features.

WHEN THIS EXTRACTOR IS CHOSEN
------------------------------
DocumentRouter calls can_handle() which returns True for .pdf files.
The router then calls extract() and inspects char density.
If density >= ocr_char_density_threshold → this result is used.
If density < threshold → OcrExtractor is tried instead (auto-detect).

LIBRARY: pdfminer.six
---------------------
pdfminer.six is chosen over PyMuPDF because:
    - Pure Python (no C binary dependency)
    - Preserves reading order via LAParams
    - License: MIT (no GPL concerns)
    - Gives character bounding boxes (useful for Phase 3 highlighting)

WHAT IS EXTRACTED
-----------------
- All text from all pages, in reading order
- Page break markers inserted as "\n\n--- PAGE {n} ---\n\n"
  (TextCleaner can strip or preserve these)
- PDF metadata stored in ExtractionResult.metadata:
    {
        "producer": "Adobe Acrobat",
        "creator": "Word",
        "creation_date": "2024-01-15",
        "total_pages": 12,
        "char_density": 450.3   # average chars per page
    }

KNOWN LIMITATIONS
-----------------
- Does NOT handle password-protected PDFs (raises ExtractionError)
- Does NOT handle PDFs with embedded fonts that map to private use area glyphs
  (TextCleaner's ligature fixer handles most common cases)
- Table extraction is NOT layout-aware (use camelot in Phase 3 if needed)

IMPLEMENTATION NOTES
--------------------
- Use high_level.extract_text() for simple cases
- Use PDFPageInterpreter + PDFConverter for per-page extraction with metadata
- Wrap all pdfminer errors in ExtractionError with path and page context
- Log each page processed at DEBUG level (not INFO — too verbose for production)

USAGE EXAMPLE
-------------
    from ingestion.pdf_extractor import PdfExtractor
    from pathlib import Path

    extractor = PdfExtractor()
    result = extractor.extract(Path("contracts/acme.pdf"))
    print(result.raw_text[:200])
    print(result.metadata["char_density"])
"""

from __future__ import annotations

from pathlib import Path

from core.exceptions import ExtractionError  # noqa: F401 (used in implementation)
from core.logging import get_logger
from core.types import ExtractionMethod, ExtractionResult

log = get_logger(__name__)


class PdfExtractor:
    """
    Extracts text from digital (text-layer) PDF files using pdfminer.six.

    Implements the BaseExtractor Protocol — no explicit inheritance needed.

    Attributes
    ----------
    _laparams : LAParams
        pdfminer layout analysis parameters. Configured for contracts:
        - line_margin=0.5 to handle tight legal line spacing
        - word_margin=0.1 to avoid splitting hyphenated words
        - detect_vertical=False (contracts are horizontal text only)

    THREAD SAFETY
    -------------
    PdfExtractor instances are stateless between calls — safe to share
    across threads. Each extract() call creates its own pdfminer objects.
    """

    SUPPORTED_EXTENSIONS: frozenset[str] = frozenset({".pdf"})

    def can_handle(self, path: Path) -> bool:
        """
        Return True for .pdf files regardless of whether they are digital or scanned.

        DocumentRouter will call extract() first; if char density is too low,
        it will fall back to OcrExtractor. This extractor always tries first.

        Parameters
        ----------
        path : Path
            File path to check.

        Returns
        -------
        bool
            True if path has a .pdf extension (case-insensitive).
        """
        # TODO (implementation): return path.suffix.lower() in self.SUPPORTED_EXTENSIONS
        pass

    def extract(self, path: Path) -> ExtractionResult:
        """
        Extract text page-by-page from a digital PDF.

        Algorithm
        ---------
        1. Open PDF with pdfminer PDFPage.get_pages()
        2. For each page:
            a. Run PDFPageInterpreter to extract text blocks
            b. Append page text + PAGE MARKER to output buffer
            c. Track character count for density calculation
        3. Extract PDF metadata (producer, creator, dates)
        4. Calculate char_density = total_chars / page_count
        5. Return ExtractionResult with all collected data

        Parameters
        ----------
        path : Path
            Absolute path to the PDF file.

        Returns
        -------
        ExtractionResult
            raw_text: full text with page markers
            method: ExtractionMethod.PDF_DIRECT
            page_count: number of pages processed
            metadata: {producer, creator, creation_date, total_pages, char_density}

        Raises
        ------
        ExtractionError
            - If path does not exist
            - If PDF is encrypted / password-protected
            - If pdfminer raises PDFException or PDFSyntaxError
            Wraps original exception with path context.
        """
        # TODO (implementation): full pdfminer.six extraction logic
        pass
