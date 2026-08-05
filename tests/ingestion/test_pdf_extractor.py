"""
tests/ingestion/test_pdf_extractor.py
=======================================
Unit tests for ingestion/pdf_extractor.py — PdfExtractor class.

WHAT IS TESTED
--------------
1. can_handle()
   - Returns True for .pdf extension (upper and lower case)
   - Returns False for .docx, .txt, .png

2. extract() — happy path (digital PDF)
   - Returns ExtractionResult with non-empty raw_text
   - method == ExtractionMethod.PDF_DIRECT
   - page_count >= 1
   - metadata contains "char_density" key

3. extract() — error cases
   - Raises ExtractionError when file does not exist
   - Raises ExtractionError when file is encrypted (password-protected)
   - Raises ExtractionError when file is corrupt (invalid PDF bytes)

4. char_density calculation
   - density = total_chars / page_count
   - Verifies that a known digital PDF produces density > 50

TEST STRATEGY
-------------
- Use the minimal_digital.pdf fixture from tests/fixtures/
- For error cases: create temp files with invalid content using tmp_path
- Do NOT mock pdfminer internals — test real behaviour against fixture files
  (pdfminer is a pure Python library, no external binary needed)

MARKS
-----
@pytest.mark.unit        — all tests here are unit-level
@pytest.mark.slow        — mark any test that opens a large PDF
"""

from __future__ import annotations

import pytest
from pathlib import Path

# TODO (implementation): import PdfExtractor, ExtractionMethod, ExtractionError


class TestPdfExtractorCanHandle:
    """Tests for PdfExtractor.can_handle()."""

    def test_returns_true_for_pdf_lowercase(self):
        """can_handle() returns True for .pdf extension."""
        # TODO: extractor = PdfExtractor()
        #       assert extractor.can_handle(Path("contract.pdf")) is True
        pass

    def test_returns_true_for_pdf_uppercase(self):
        """can_handle() is case-insensitive (.PDF → True)."""
        pass

    def test_returns_false_for_docx(self):
        """can_handle() returns False for .docx."""
        pass

    def test_returns_false_for_txt(self):
        """can_handle() returns False for .txt."""
        pass


class TestPdfExtractorExtract:
    """Tests for PdfExtractor.extract() — happy path."""

    def test_extract_returns_nonempty_text(self, sample_pdf_path):
        """extract() produces non-empty raw_text for a valid digital PDF."""
        pass

    def test_extract_method_is_pdf_direct(self, sample_pdf_path):
        """result.method == ExtractionMethod.PDF_DIRECT for digital PDF."""
        pass

    def test_extract_page_count_gte_one(self, sample_pdf_path):
        """result.page_count >= 1."""
        pass

    def test_extract_metadata_has_char_density(self, sample_pdf_path):
        """result.metadata contains 'char_density' key."""
        pass

    def test_char_density_above_threshold_for_digital_pdf(self, sample_pdf_path):
        """Digital PDF produces char_density > 50 (above OCR fallback threshold)."""
        pass


class TestPdfExtractorErrors:
    """Tests for PdfExtractor.extract() — error conditions."""

    def test_raises_extraction_error_when_file_missing(self, tmp_path):
        """extract() raises ExtractionError if file does not exist."""
        pass

    def test_raises_extraction_error_for_corrupt_pdf(self, tmp_path):
        """extract() raises ExtractionError for a file with invalid PDF bytes."""
        # Write b"NOT_A_PDF" to a .pdf file and verify ExtractionError is raised
        pass
