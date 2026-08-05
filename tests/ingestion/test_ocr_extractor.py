"""
tests/ingestion/test_ocr_extractor.py
=======================================
Unit tests for ingestion/ocr_extractor.py — OcrExtractor class.

WHAT IS TESTED
--------------
1. can_handle()
   - Same as PdfExtractor (True for .pdf only)

2. _preprocess_image()
   - Returns a PIL Image in 'L' (greyscale) mode
   - Output image has same dimensions as input (no accidental resize)
   - Can be called with a solid-colour PIL Image (no crash)

3. extract() — integration (requires poppler + tesseract)
   - Returns ExtractionResult with non-empty raw_text
   - method == ExtractionMethod.PDF_OCR
   - metadata contains "avg_confidence" and "ocr_engine" keys
   - avg_confidence is a float in [0.0, 100.0]

4. extract() — error cases
   - Raises OCRError if pdf2image cannot find poppler binary
   - Individual page failure inserts "[PAGE {n} OCR FAILED]" marker
     (does not crash the whole extraction)

TEST MARKS
----------
@pytest.mark.integration  — tests that call real Tesseract/poppler
@pytest.mark.unit         — _preprocess_image tests (pure PIL, no binary)

SKIPPING INTEGRATION TESTS
---------------------------
OCR integration tests are skipped automatically if tesseract is not installed:
    pytestmark = pytest.mark.skipif(
        shutil.which("tesseract") is None,
        reason="Tesseract not installed"
    )
"""

from __future__ import annotations

import shutil

import pytest
from PIL import Image

# TODO (implementation): import OcrExtractor, ExtractionMethod, OCRError

pytestmark = pytest.mark.skipif(
    shutil.which("tesseract") is None,
    reason="Tesseract OCR binary not installed — skipping OCR tests",
)


class TestOcrExtractorPreprocess:
    """Tests for OcrExtractor._preprocess_image() — pure PIL, no Tesseract needed."""

    def test_returns_greyscale_image(self):
        """_preprocess_image() converts RGB image to greyscale (mode='L')."""
        # Create a synthetic 100×100 white RGB image
        # img = Image.new("RGB", (100, 100), color=(255, 255, 255))
        # extractor = OcrExtractor()
        # result = extractor._preprocess_image(img)
        # assert result.mode == "L"
        pass

    def test_preserves_dimensions(self):
        """Output image has same pixel dimensions as input."""
        pass

    def test_handles_solid_black_image(self):
        """Does not crash on an all-black image (zero contrast edge case)."""
        pass

    def test_handles_solid_white_image(self):
        """Does not crash on an all-white image (blank page edge case)."""
        pass


class TestOcrExtractorExtract:
    """Integration tests for OcrExtractor.extract() — requires Tesseract + poppler."""

    def test_extract_returns_nonempty_text(self, sample_scanned_pdf_path):
        """OCR extraction produces non-empty raw_text from a scanned PDF."""
        pass

    def test_extract_method_is_pdf_ocr(self, sample_scanned_pdf_path):
        """result.method == ExtractionMethod.PDF_OCR."""
        pass

    def test_extract_avg_confidence_in_valid_range(self, sample_scanned_pdf_path):
        """avg_confidence is a float between 0.0 and 100.0."""
        pass

    def test_extract_metadata_has_ocr_engine(self, sample_scanned_pdf_path):
        """result.metadata['ocr_engine'] == 'tesseract'."""
        pass
