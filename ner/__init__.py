"""
ner/
====
spaCy NER training, evaluation, and inference package.

PURPOSE
-------
This package contains everything needed to:
    1. Train a spaCy NER model on the processed CUAD data (train.py)
    2. Evaluate model performance per entity type (evaluate.py)
    3. Load the model and run inference on new text (inference.py)

This package is the consumer of data_processing outputs.
It is the producer of model artifacts consumed by Phase 3 (API).

WHAT IT DOES NOT DO
-------------------
- Does not know about PDF files or document types (that's ingestion/)
- Does not process raw CUAD data (that's data_processing/)
- Does not serve HTTP requests (that's Phase 3 — api/)

PUBLIC API
----------
    from ner import NERModel, load_model

    model = load_model("models/ner_baseline")
    entities = model.extract_entities("This Agreement between Acme Corp...")

INTERNAL MODULES
----------------
    base.py             BaseNERModel Protocol
    train.py            Entry-point: train and save the model
    evaluate.py         Per-entity-type P/R/F1 evaluation
    inference.py        NERModel class — load model, run inference

TRAINING ARTIFACT LOCATION
---------------------------
    models/ner_baseline/    → saved by train.py
        meta.json           → spaCy model metadata (labels, version, date)
        config.cfg          → training configuration
        vocab/              → vocabulary + word vectors
        ner/                → NER component weights

MODEL VERSIONING (Phase 3+)
----------------------------
In Phase 3, model artifacts will be versioned by timestamp:
    models/ner_baseline_20250810_143022/
For now (Phase 1), a single models/ner_baseline/ directory is sufficient.
"""

from ner.inference import NERModel, load_model

__all__ = ["NERModel", "load_model"]
