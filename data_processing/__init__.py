"""
data_processing/
================
CUAD dataset processing pipeline — raw dataset → training artifacts.

PURPOSE
-------
Transforms the raw CUAD (Contract Understanding Atticus Dataset) into two
training artifact formats:

    1. spaCy DocBin  (.spacy binary) → consumed by ner/train.py
    2. Clause JSON   (.json)         → consumed by Phase-2 transformer fine-tuning

This package knows about CUAD's structure and training formats.
It does NOT know about extractors, models, or the API layer.

PIPELINE OVERVIEW
-----------------
    HuggingFace CUAD dataset
            │
            ▼
    CuadLoader.load()              → list[dict]  (raw CUAD samples)
            │
            ├──▶ CuadToNer.convert()         → list[NERSample]
            │         │
            │         ▼
            │   SpanValidator.validate()     → cleaned list[NERSample]
            │         │
            │         ▼
            │   DocBin → cuad_ner_train.spacy / cuad_ner_dev.spacy
            │
            └──▶ CuadToClassification.convert()  → list[ClauseSample]
                        │
                        ▼
                  cuad_clauses_train.json / cuad_clauses_dev.json

INTERNAL MODULES
----------------
    base.py                     BaseConverter Protocol
    cuad_loader.py              CUAD dataset loading + train/dev split
    cuad_to_ner.py              CUAD Q&A → spaCy NER spans
    cuad_to_classification.py   CUAD Q&A → clause classification JSON
    span_validator.py           Overlapping span resolution
    dataset_stats.py            Distribution statistics + reports

PUBLIC API (what callers import)
---------------------------------
    from data_processing import load_cuad, build_ner_corpus, build_clause_corpus
"""

from data_processing.cuad_loader import load_cuad
from data_processing.cuad_to_ner import build_ner_corpus
from data_processing.cuad_to_classification import build_clause_corpus

__all__ = ["load_cuad", "build_ner_corpus", "build_clause_corpus"]
