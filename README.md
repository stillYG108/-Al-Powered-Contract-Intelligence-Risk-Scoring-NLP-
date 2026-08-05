# AI-Powered Contract Intelligence & Risk Scoring

> **Phase 1**: Data Parsing & Baseline Modeling

---

## Project Architecture

```
contract-intelligence/
├── core/                    ← Foundation: types, config, logging, exceptions
├── ingestion/               ← Document → clean text (PDF, OCR, DOCX, TXT)
├── data_processing/         ← CUAD dataset → spaCy training artifacts
├── ner/                     ← NER model training, evaluation, and inference
├── models/                  ← Saved model artifacts (gitignored)
├── data/                    ← Raw + processed training data (gitignored)
├── tests/                   ← Pytest test suite (mirrors src structure)
└── scripts/                 ← Shell scripts for pipeline orchestration
```

**Dependency rule**: `core ← ingestion, data_processing, ner ← tests`
No sibling package imports another sibling. All shared types flow through `core/`.

---

## Phase Roadmap

| Phase | Week | Focus |
|---|---|---|
| **1 (current)** | 1 | CUAD processing · OCR pipeline · spaCy NER baseline |
| 2 | 2 | RoBERTa-legal fine-tuning · clause classification |
| 3 | 3 | Vector search (Pinecone/Milvus) · FastAPI + Celery |
| 4 | 4 | Docker · AWS EC2 · Frontend highlights UI |

---

## Quick Start

```bash
# 1. Clone and set up environment
git clone <repo>
cd contract-intelligence
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt

# 2. Configure
cp .env.example .env
# Edit .env as needed

# 3. Install spaCy base model
python -m spacy download en_core_web_lg

# 4. Download CUAD dataset
bash scripts/download_cuad.sh

# 5. Process training data
bash scripts/prepare_data.sh

# 6. Train NER baseline
bash scripts/train_ner.sh

# 7. Evaluate
python -m ner.evaluate --model models/ner_baseline --dev data/processed/cuad_ner_dev.spacy

# 8. Run tests
pytest tests/ -v --cov
```

---

## System Requirements

| Dependency | Version | Installation |
|---|---|---|
| Python | 3.11+ | pyenv or system |
| Tesseract | 5.x | `apt install tesseract-ocr` / `brew install tesseract` |
| poppler | any | `apt install poppler-utils` / `brew install poppler` |
| GPU | optional | Set `GPU_ID=0` in `.env` for faster training |

---

## Key Design Decisions (Phase 1)

- **All 41 CUAD clause types** mapped to NER labels (future-proofed for Phase 2)
- **Auto-detect scanned PDFs**: pdfminer first → OCR fallback if char density < 50/page
- **Span conflict resolution**: keep longer span, log every discard as structured audit record
- **CPU-only training**: `GPU_ID=-1` (upgrade in Phase 2 with transformer models)
- **Protocol interfaces**: `BaseExtractor`, `BaseConverter`, `BaseNERModel` — loose coupling across phases

---

## Environment Variables

See [`.env.example`](.env.example) for full documentation of all configuration options.

---

## Running Tests

```bash
# All tests
pytest tests/ -v

# Unit tests only (no Tesseract/model required)
pytest tests/ -m unit -v

# With coverage
pytest tests/ --cov=core --cov=ingestion --cov=data_processing --cov=ner
```
