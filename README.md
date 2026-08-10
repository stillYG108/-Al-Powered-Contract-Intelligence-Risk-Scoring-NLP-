# -Al-Powered-Contract-Intelligence-Risk-Scoring-NLP-

# Ingestion Pipeline

## Overview

The `ingestion/` module extracts and cleans text from PDF and DOCX contracts. It automatically detects scanned PDF pages and uses OCR when required.

## Pipeline

```text
Input File
    |
    ▼
DocumentRouter
    |
    ├── PDF ──► PdfExtractor
    │              |
    │              └── < 50 chars ──► OcrExtractor
    |
    └── DOCX ──► DocxExtractor
                       |
                       ▼
                  TextCleaner
                       |
                       ▼
                  Clean Text
```

## Components

### `pdf_extractor.py`

* Uses **pdfminer.six**.
* Extracts PDF text page-by-page.
* Flags pages with `< 50` characters.
* Sends flagged pages for OCR.

### `ocr_extractor.py`

* Uses **pdf2image + OpenCV + Tesseract**.
* Converts PDF pages to images at **300 DPI**.
* Applies grayscale, thresholding, and denoising.
* Uses:

```text
--oem 3 --psm 6
```

### `docx_extractor.py`

* Uses **python-docx**.
* Extracts paragraphs and tables.
* Preserves basic reading order.

### `document_router.py`

* Detects PDF/DOCX.
* Routes files to the correct extractor.
* Sends low-text PDF pages to OCR.

### `text_cleaner.py`

* Fixes ligatures.
* Normalizes whitespace.
* Removes repeated headers/footers.
* Returns word count and extraction metadata.

## Structure

```text
ingestion/
├── __init__.py
├── pdf_extractor.py
├── ocr_extractor.py
├── docx_extractor.py
├── document_router.py
└── text_cleaner.py
```

## Dependencies

```bash
pip install pdfminer.six pdf2image pytesseract pillow opencv-python numpy python-docx
```

**System requirements:** Tesseract OCR and Poppler.

## Purpose

Converts digital PDFs, scanned PDFs, and DOCX contracts into clean, machine-readable text for the downstream NLP/NER pipeline.



<img width="1463" height="889" alt="final" src="https://github.com/user-attachments/assets/87a1074c-4168-4895-9b13-b34bd5be0a5c" />
