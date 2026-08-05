"""
ingestion/ocr_extractor.py
==========================
Text extractor for SCANNED PDF files (image-only, no text layer).

PURPOSE
-------
Handles PDFs that are scans of physical documents — no selectable text exists.
Renders each page as a high-resolution image then runs Tesseract OCR on it.

WHEN THIS EXTRACTOR IS CHOSEN
------------------------------
DocumentRouter uses AUTO-DETECT mode (Phase 1 decision):
1. PdfExtractor.extract() is called first on every .pdf file.
2. Router computes char_density = chars / pages from PdfExtractor result.
3. If char_density < settings.ocr_char_density_threshold (default: 50):
   → this file is considered scanned → OcrExtractor.extract() is called.
4. OcrExtractor result replaces the PdfExtractor result.

PIPELINE (per page)
-------------------
    PDF page
        │
        ▼ pdf2image.convert_from_path(dpi=300)
    PIL.Image (RGB, 300 DPI)
        │
        ▼ _preprocess_image()
    PIL.Image (enhanced for OCR)
        │  Steps:
        │    1. Convert to greyscale (L mode)
        │    2. ImageOps.autocontrast() — normalise brightness
        │    3. ImageFilter.SHARPEN × 1 pass — improve character edges
        │    4. ImageEnhance.Contrast(factor=1.5) — increase contrast
        │    5. Resize to ≥300 DPI if original is lower
        │
        ▼ pytesseract.image_to_string(lang=settings.ocr_lang, config=OEM+PSM)
    raw OCR text (str)
        │
        ▼ collected per page, joined with PAGE MARKERS
    ExtractionResult

TESSERACT CONFIG
----------------
OEM 3  — LSTM + Legacy engine (best accuracy)
PSM 3  — Fully automatic page segmentation (good for multi-column contracts)

WHY pdf2image + PIL (not PyMuPDF)
----------------------------------
- pdf2image uses poppler which handles edge cases PyMuPDF misses
- PIL preprocessing is easily testable (pure image transforms)
- No dependency conflicts with pdfminer.six

METADATA INCLUDED IN RESULT
----------------------------
{
    "ocr_engine": "tesseract",
    "tesseract_version": "5.3.1",
    "dpi": 300,
    "lang": "eng",
    "avg_confidence": 87.4,   # mean of per-page pytesseract confidence scores
    "low_confidence_pages": [3, 7]  # pages below 60% confidence (logged as warnings)
}

IMPLEMENTATION NOTES
--------------------
- Use tqdm to show per-page progress in scripts (not in API mode)
- Page confidence extracted via pytesseract.image_to_data(output_type=Output.DICT)
- If a single page fails OCR, log warning + insert "[PAGE {n} OCR FAILED]" marker
  (do not abort the entire document)
- Tesseract binary path set from settings.tesseract_cmd (empty = auto-detect)

USAGE EXAMPLE
-------------
    from ingestion.ocr_extractor import OcrExtractor
    from pathlib import Path

    extractor = OcrExtractor()
    result = extractor.extract(Path("scanned_contract.pdf"))
    print(result.metadata["avg_confidence"])  # e.g. 87.4
"""

from __future__ import annotations

from pathlib import Path

from core.exceptions import OCRError  # noqa: F401
from core.logging import get_logger
from core.types import ExtractionMethod, ExtractionResult

log = get_logger(__name__)


class OcrExtractor:
    """
    OCR-based text extractor for scanned PDF files.

    Implements the BaseExtractor Protocol.

    Attributes
    ----------
    _dpi : int
        Render resolution for pdf2image (from settings.ocr_dpi, default 300).
    _lang : str
        Tesseract language (from settings.ocr_lang, default "eng").
    _tesseract_cmd : str
        Path to tesseract binary; empty string means auto-detect via shutil.which.

    THREAD SAFETY
    -------------
    OcrExtractor is stateless between extract() calls — safe to share.
    Tesseract subprocess is spawned fresh per page (pytesseract default).
    """

    SUPPORTED_EXTENSIONS: frozenset[str] = frozenset({".pdf"})

    def can_handle(self, path: Path) -> bool:
        """
        Return True for .pdf files.

        OcrExtractor is tried ONLY when DocumentRouter decides the PDF is scanned
        (char density too low). The can_handle() check is the same as PdfExtractor;
        selection between them is done by the router's density heuristic.
        """
        # TODO (implementation): return path.suffix.lower() in self.SUPPORTED_EXTENSIONS
        pass

    def extract(self, path: Path) -> ExtractionResult:
        """
        Render each PDF page to an image and run Tesseract OCR.

        Algorithm
        ---------
        1. Use pdf2image.convert_from_path(path, dpi=self._dpi) to get PIL images.
        2. For each page image:
            a. _preprocess_image(image) → enhanced PIL image
            b. pytesseract.image_to_string() → page_text
            c. pytesseract.image_to_data() → per-word confidence scores
            d. Compute page confidence = mean of word-level confidence values
            e. If page_confidence < 60: log warning, add to low_confidence_pages
            f. Append page_text + PAGE MARKER to output buffer
        3. Calculate avg_confidence across all pages.
        4. Build and return ExtractionResult.

        Parameters
        ----------
        path : Path
            Absolute path to the scanned PDF.

        Returns
        -------
        ExtractionResult
            raw_text: OCR'd text with page markers
            method: ExtractionMethod.PDF_OCR
            page_count: number of pages rendered
            metadata: {ocr_engine, tesseract_version, dpi, lang,
                        avg_confidence, low_confidence_pages}

        Raises
        ------
        OCRError
            - If pdf2image fails (poppler not installed, file corrupted)
            - If tesseract binary not found or crashes with non-zero exit
            Original exception is chained via `raise OCRError(...) from exc`
        ExtractionError
            If path does not exist or is empty.
        """
        # TODO (implementation): full OCR pipeline
        pass

    def _preprocess_image(self, image):  # PIL.Image.Image → PIL.Image.Image
        """
        Apply image enhancement transforms to improve Tesseract accuracy.

        Transforms applied IN ORDER:
        1. image.convert("L")                   — convert RGB → greyscale
        2. ImageOps.autocontrast(image)          — stretch contrast to full range
        3. image.filter(ImageFilter.SHARPEN)     — one sharpen pass
        4. ImageEnhance.Contrast(image).enhance(1.5) — boost contrast ×1.5
        5. Check DPI; if < 300, resize to 300 DPI equivalent

        Parameters
        ----------
        image : PIL.Image.Image
            Raw RGB page render from pdf2image.

        Returns
        -------
        PIL.Image.Image
            Preprocessed greyscale image ready for Tesseract.

        TESTING NOTE
        ------------
        This method is pure (no I/O) → test it with synthetic PIL images.
        See tests/ingestion/test_ocr_extractor.py::test_preprocess_image_*
        """
        # TODO (implementation): apply PIL transforms
        pass
