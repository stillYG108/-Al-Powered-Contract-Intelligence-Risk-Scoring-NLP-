"""
ingestion/document_router.py
=============================
Routes an input file to the correct extractor — the Strategy pattern hub.

PURPOSE
-------
This is the ONLY module callers interact with in the ingestion layer.
It hides all extractor selection logic behind a single .route(path) call.

Callers never import PdfExtractor, OcrExtractor, etc. directly.

DESIGN PATTERN: Strategy
--------------------------
DocumentRouter holds a list of extractor instances (the "strategies").
For each file, it selects the first extractor whose can_handle() returns True,
then calls extract().

For PDFs specifically, it applies an AUTO-DETECT heuristic:
    1. Try PdfExtractor first
    2. Measure char density (chars / pages) of the result
    3. If density < settings.ocr_char_density_threshold (default: 50):
       → file is a scanned PDF → retry with OcrExtractor
    4. Log which extractor was ultimately used and char density

AUTO-DETECT FLOW (PDF only)
-----------------------------
    .pdf file
        │
        ▼ PdfExtractor.extract()
    ExtractionResult
        │
        ├─ char_density >= 50 → ✓ use this result (DocumentType.PDF_DIGITAL)
        │
        └─ char_density < 50  → retry with OcrExtractor
                                    │
                                    ▼ OcrExtractor.extract()
                                ExtractionResult (DocumentType.PDF_SCANNED)

EXTRACTOR REGISTRY
------------------
Extractors are registered in priority order in __init__:
    1. DocxExtractor    (fast, definitive for .docx)
    2. TextExtractor    (fast, definitive for .txt/.md)
    3. PdfExtractor     (tries first for all .pdf)
    4. TextExtractor    (fallback — registered last as catch-all)

ADDING A NEW EXTRACTOR
----------------------
1. Create NewExtractor in ingestion/new_extractor.py implementing BaseExtractor
2. Import it here
3. Add it to self._extractors list in __init__ at the right priority position
4. DocumentRouter.route() works without any other changes — fully Open/Closed

USAGE EXAMPLE
-------------
    from ingestion import DocumentRouter

    router = DocumentRouter()                          # default config
    result = router.route("contracts/merger_doc.pdf")  # auto-detects type
    print(result.method)    # "pdf_direct" or "pdf_ocr"
    print(result.raw_text[:100])
"""

from __future__ import annotations

from pathlib import Path

from core.config import get_settings
from core.exceptions import UnsupportedFileTypeError  # noqa: F401
from core.logging import get_logger
from core.types import ExtractionResult
from ingestion.base import BaseExtractor

log = get_logger(__name__)


class DocumentRouter:
    """
    Routes a document file to its correct extractor.

    Implements the Strategy pattern. Callers use ONLY this class from
    the ingestion package.

    Parameters
    ----------
    extractors : list[BaseExtractor] | None
        Optional list of extractors to use, in priority order.
        If None, the default registry (DocxExtractor, PdfExtractor,
        OcrExtractor, TextExtractor) is instantiated.
        Passing a custom list allows easy mocking in tests.

    ocr_density_threshold : int | None
        Chars-per-page threshold below which a PDF is treated as scanned.
        If None, reads from settings.ocr_char_density_threshold (default: 50).

    USAGE IN TESTS
    --------------
    # Mock extractors without hitting disk:
    mock_pdf = Mock(spec=BaseExtractor)
    mock_pdf.can_handle.return_value = True
    mock_pdf.extract.return_value = ExtractionResult(...)
    router = DocumentRouter(extractors=[mock_pdf])
    result = router.route("any.pdf")
    """

    def __init__(
        self,
        extractors: list[BaseExtractor] | None = None,
        ocr_density_threshold: int | None = None,
    ) -> None:
        """
        Initialise the router with an extractor registry.

        IMPLEMENTATION NOTES
        --------------------
        - If extractors is None, build default registry:
            from ingestion.docx_extractor import DocxExtractor
            from ingestion.pdf_extractor import PdfExtractor
            from ingestion.ocr_extractor import OcrExtractor
            from ingestion.text_extractor import TextExtractor
            self._extractors = [DocxExtractor(), PdfExtractor(), OcrExtractor(), TextExtractor()]
        - Store ocr_density_threshold from param or settings
        - Log registered extractor class names at DEBUG level
        """
        # TODO (implementation): build extractor registry
        pass

    def route(self, path: str | Path) -> ExtractionResult:
        """
        Route `path` to the correct extractor and return extracted text.

        This is the SINGLE PUBLIC METHOD callers use.

        Algorithm
        ---------
        1. Normalise input to pathlib.Path
        2. Verify file exists → raise ExtractionError if not
        3. Iterate self._extractors: find first where can_handle(path) is True
        4. Call extractor.extract(path) → result
        5. If result came from PdfExtractor:
            a. Compute char_density from result.metadata["char_density"]
            b. If density < self._ocr_density_threshold:
                → log.info("scanned_pdf_detected", ...)
                → call OcrExtractor.extract(path) instead
                → replace result with OCR result
        6. Log final method used, char_density, page_count
        7. Return result

        Parameters
        ----------
        path : str | Path
            Path to the input document.

        Returns
        -------
        ExtractionResult
            Always contains non-empty raw_text (or raises).

        Raises
        ------
        ExtractionError
            If path does not exist.
        UnsupportedFileTypeError
            If no extractor in the registry can handle the file type.
        OCRError / ExtractionError
            If the selected extractor fails internally.
        """
        # TODO (implementation): routing logic with OCR auto-detect
        pass
