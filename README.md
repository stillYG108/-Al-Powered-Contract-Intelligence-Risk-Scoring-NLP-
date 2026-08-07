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



# Scanned PDF OCR Extractor (`ocr_extractor.py`)

## Overview

`ocr_extractor.py` extracts text from scanned PDF documents using OCR. It converts PDF pages into high-resolution images, applies image preprocessing, and uses Tesseract OCR for accurate text recognition.

## Features

* Converts PDF pages to images using `pdf2image` at **300 DPI**.
* Applies image preprocessing:

  * Grayscale conversion.
  * Adaptive thresholding.
  * Deskewing using Tesseract OSD.
  * Noise removal.
* Performs OCR using Tesseract.
* Reassembles extracted text page-by-page.

## OCR Pipeline

```
PDF Page
   |
   ▼
pdf2image.convert_from_path(dpi=300)
   |
   ▼
PIL Image (RGB)
   |
   ▼
Image Preprocessing
   ├── Grayscale
   ├── Adaptive Thresholding
   ├── Deskew
   └── Denoising
   |
   ▼
Tesseract OCR
   |
   ▼
Extracted Text
   |
   ▼
Combined Document Text
```

## Tesseract Configuration

```
--oem 3
--psm 6
```

* `--oem 3` → Uses LSTM + legacy OCR engine.
* `--psm 6` → Assumes a uniform block of text.

## Output

Returns:

* OCR-extracted text from scanned PDF pages.
* Page-separated document text format:

```
--- PAGE 1 ---

Extracted text...

--- PAGE 2 ---

Extracted text...
```

## Dependencies

```bash
pip install pdf2image pytesseract pillow opencv-python
```

System requirements:

* Poppler
* Tesseract OCR

## Purpose

Handles scanned documents that cannot be processed using normal PDF text extraction and provides clean text for downstream NLP pipelines.
<img width="1591" height="319" alt="Screenshot 2026-08-07 210747" src="https://github.com/user-attachments/assets/448b867a-5027-4b8f-bc56-38c8aa87bed2" />

