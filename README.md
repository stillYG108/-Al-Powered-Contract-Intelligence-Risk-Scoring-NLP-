# -Al-Powered-Contract-Intelligence-Risk-Scoring-NLP-

# Digital PDF Extractor (`pdf_extractor.py`)

## Overview

`pdf_extractor.py` extracts text from digital PDF documents using **pdfminer.six**. It processes PDFs page-by-page and identifies pages that may contain scanned images instead of extractable text.

## Features

* Extracts text from each PDF page using `pdfminer.six`.
* Performs page-level text extraction.
* Detects likely scanned pages.
* Flags pages with fewer than **50 characters** of extracted text.
* Returns flagged page numbers for OCR processing.

## Workflow

```
PDF Document
      |
      ▼
pdfminer.six Text Extraction
      |
      ▼
Page-wise Text Analysis
      |
      ▼
Check Extracted Text Length
      |
      ├── >= 50 characters → Digital Text Page
      |
      └── < 50 characters → Flag as Scanned Page
```

## Output

Returns:

* Extracted text from digital PDF pages.
* List of flagged page numbers requiring OCR extraction.

## Dependencies

```bash
pip install pdfminer.six
```

## Purpose

Acts as the first stage of the document processing pipeline and routes scanned pages to `ocr_extractor.py` for OCR-based extraction.
<img width="1591" height="319" alt="Screenshot 2026-08-07 210747" src="https://github.com/user-attachments/assets/26ec2ba0-a615-4bbd-81f7-ca1c6f5d31cd" />

