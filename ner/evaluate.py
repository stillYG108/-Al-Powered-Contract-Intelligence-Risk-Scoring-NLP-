"""
ner/evaluate.py
================
Per-entity-type precision, recall, and F1 evaluation on the dev set.

PURPOSE
-------
Provides an independent evaluation script and a programmatic API
for computing NER metrics without running the full training pipeline.

INVOCATION
----------
    python -m ner.evaluate --model models/ner_baseline --dev data/processed/cuad_ner_dev.spacy

METRICS COMPUTED
----------------
For each entity label:
    Precision  = TP / (TP + FP)   — "of all predicted spans, how many were correct?"
    Recall     = TP / (TP + FN)   — "of all gold spans, how many were found?"
    F1         = 2 × P × R / (P + R)  — harmonic mean

Overall (micro and macro):
    Micro F1   = F1 computed on pooled TP/FP/FN counts (favours frequent labels)
    Macro F1   = mean of per-label F1 scores (treats all labels equally)

SPAN MATCHING STRATEGY
-----------------------
Exact match: a predicted span is correct only if BOTH start AND end
character offsets AND label match the gold annotation exactly.

Rationale: CUAD annotations are precise; partial credit creates ambiguity
and makes comparison across models harder. Partial match can be added
in Phase 2 if needed.

OUTPUT FORMAT
-------------
Prints to stdout:
    ══════════════════════════════════════════════════════
     NER Evaluation — models/ner_baseline
     Dev set: data/processed/cuad_ner_dev.spacy (1477 samples)
    ══════════════════════════════════════════════════════
     Label                          P       R      F1   Support
    ──────────────────────────────────────────────────────────
     PARTIES                     0.912   0.887   0.899     412
     GOVERNING_LAW               0.871   0.903   0.887     284
     EXPIRATION_DATE              0.834   0.761   0.796     201
     ...
    ──────────────────────────────────────────────────────────
     MICRO AVG                   0.856   0.831   0.843    3421
     MACRO AVG                   0.841   0.818   0.829      —
    ══════════════════════════════════════════════════════

Also writes metrics to JSON: models/ner_baseline/eval_metrics.json

INTEGRATION WITH TRAINING
--------------------------
train.py calls compute_metrics() in _post_training_steps().
The return value (dict) is stored in training_meta.json.
"""

from __future__ import annotations

from pathlib import Path

from core.logging import get_logger, configure_logging
from core.types import Entity

log = get_logger(__name__)


def compute_metrics(
    model_path: Path,
    dev_path: Path,
) -> dict:
    """
    Compute per-label P/R/F1 metrics and overall micro/macro averages.

    Parameters
    ----------
    model_path : Path
        Path to the saved spaCy model directory.
    dev_path : Path
        Path to the cuad_ner_dev.spacy DocBin file.

    Returns
    -------
    dict
        {
            "per_label": {
                "PARTIES": {"precision": 0.912, "recall": 0.887, "f1": 0.899, "support": 412},
                ...
            },
            "micro": {"precision": 0.856, "recall": 0.831, "f1": 0.843},
            "macro": {"precision": 0.841, "recall": 0.818, "f1": 0.829},
            "total_samples": 1477,
            "total_entities": 3421,
        }

    ALGORITHM
    ---------
    1. Load model: spacy.load(model_path)
    2. Load dev DocBin → list of gold Doc objects
    3. For each gold Doc:
        a. Run nlp(doc.text) → predicted Doc
        b. Compare pred.ents vs gold doc.ents
        c. Accumulate TP, FP, FN per label
    4. Compute P/R/F1 per label from accumulated counts
    5. Compute micro and macro averages
    6. Return metrics dict

    SPAN COMPARISON
    ---------------
    Use frozenset of (start, end, label) tuples for O(1) lookup:
        gold_spans = {(e.start_char, e.end_char, e.label_) for e in doc.ents}
        pred_spans = {(e.start_char, e.end_char, e.label_) for e in pred.ents}
        tp = gold_spans & pred_spans
        fp = pred_spans - gold_spans
        fn = gold_spans - pred_spans

    Raises
    ------
    ModelNotFoundError
        If model_path does not exist.
    FileNotFoundError
        If dev_path does not exist.
    """
    # TODO (implementation)
    pass


def print_metrics_table(metrics: dict, model_path: str = "") -> None:
    """
    Print the evaluation metrics as a formatted ASCII table.

    Parameters
    ----------
    metrics : dict
        Output of compute_metrics().
    model_path : str
        Model path string to display in the header.

    IMPLEMENTATION NOTES
    --------------------
    - Sort labels by F1 descending
    - Right-align numeric columns
    - Print separator lines with ─ and ═ characters
    - Highlight labels with F1 < 0.5 with a "⚠" prefix (low quality signal)
    """
    # TODO (implementation)
    pass


def save_metrics(metrics: dict, output_path: Path) -> None:
    """
    Save metrics dict to a JSON file.

    Parameters
    ----------
    metrics : dict
        Output of compute_metrics().
    output_path : Path
        Path to write eval_metrics.json.
    """
    # TODO: json.dump(metrics, output_path.open("w"), indent=2)
    pass


def main() -> None:
    """CLI entry-point: parse args, run evaluate, print and save results."""
    configure_logging()
    # TODO: argparse for --model and --dev flags
    pass


if __name__ == "__main__":
    main()
