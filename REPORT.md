# Project Report

## AI-Powered Contract Intelligence & Risk Scoring

### Overview

This project provides a foundation for analyzing legal contracts with natural
language processing. It extracts text from PDF, scanned PDF, DOCX, and TXT
documents, then prepares contract data for named-entity recognition (NER) and
future clause-risk classification.

### Completed Work

- Processed the CUAD contract dataset into training-ready spaCy formats.
- Built document ingestion for digital PDFs, OCR-based scanned PDFs, DOCX, and
  TXT files.
- Added text cleaning, span validation, overlap resolution, and structured
  logging.
- Implemented a spaCy NER baseline for organizations, dates, money,
  jurisdictions, durations, and contract clauses.
- Added unit and integration tests for ingestion, data processing, and NER.
- Current recorded test result: **65 passed, 12 skipped, 0 failed**.

### Current Status

Phase 1 is approximately 90% complete. The remaining major task is to finish
training and evaluate the baseline NER model on the prepared CUAD data.

### Next Steps

1. Complete NER training and record evaluation metrics.
2. Fine-tune a legal language model for clause classification.
3. Add vector search and an API service.
4. Build deployment and a user interface for contract highlights and risk
   scoring.

### Technology

Python 3.11+, spaCy, Hugging Face Datasets, pdfminer.six, Tesseract,
pdf2image, python-docx, pytest, Docker, and structured logging.
