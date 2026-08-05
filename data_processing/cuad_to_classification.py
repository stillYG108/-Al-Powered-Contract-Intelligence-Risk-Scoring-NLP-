"""
data_processing/cuad_to_classification.py
==========================================
Converts CUAD Q&A annotations into clause classification training data.

PURPOSE
-------
Produces a JSON dataset where each record is a (text, label, is_present) triple.
This format is used in Phase 2 for training a RoBERTa-legal clause classifier.

We build it in Phase 1 so Phase 2 can start immediately with no data-prep work.

OUTPUT FORMAT
-------------
Files: data/processed/cuad_clauses_train.json
       data/processed/cuad_clauses_dev.json

Each file is a JSON array of ClauseSample dicts:
[
    {
        "text": "The term of this Agreement shall commence on the Effective Date...",
        "label": "RENEWAL_TERM",
        "is_present": true,
        "doc_id": "CUAD_v1/full_contract_pdf/N-1_4.pdf_0",
        "meta": {
            "question_index": 6,
            "answer_start": 2341,
            "char_count": 187
        }
    },
    ...
]

DIFFERENCE FROM NER FORMAT
---------------------------
NER format:  text = chunk,        entities = list of character spans
Clause format: text = answer text OR context window, label = clause type

For clause classification, we use the ANSWER TEXT directly as the positive
example (not the full context), because:
    - The answer IS the clause — it's the most relevant text
    - Short, focused examples train better sequence classifiers
    - Avoids the chunking complexity needed for NER

NEGATIVE EXAMPLES
-----------------
For each clause type, 50% of training examples are negatives
(contexts where the clause is absent, i.e., empty answers.text).
This creates a balanced binary classifier per clause type.

IMPLEMENTATION NOTES
--------------------
- Reuse QUESTION_TO_LABEL from cuad_to_ner.py (single source of truth)
- Write output as JSON array using json.dump with indent=2
- Compute class balance statistics after conversion and log them
- Include meta dict with question_index for traceability to CUAD source

USAGE EXAMPLE
-------------
    from data_processing.cuad_to_classification import CuadToClassification
    from pathlib import Path

    converter = CuadToClassification()
    samples = converter.convert(train_samples)
    print(samples[0].label, samples[0].is_present)

    # Module-level:
    from data_processing import build_clause_corpus
    build_clause_corpus(train_samples, dev_samples, output_dir=Path("data/processed"))
"""

from __future__ import annotations

import json
from pathlib import Path

from core.exceptions import ConversionError  # noqa: F401
from core.logging import get_logger
from core.types import ClauseSample

log = get_logger(__name__)


def build_clause_corpus(
    train_samples: list[dict],
    dev_samples: list[dict],
    output_dir: Path,
) -> None:
    """
    Module-level function: convert + write clause JSON files to disk.

    Exported from data_processing/__init__.py.

    Parameters
    ----------
    train_samples : list[dict]
        Training split from CuadLoader.load()
    dev_samples : list[dict]
        Dev split from CuadLoader.load()
    output_dir : Path
        Directory where .json files will be written.
        Files: {output_dir}/cuad_clauses_train.json, cuad_clauses_dev.json

    Side Effects
    ------------
    - Writes two JSON files to output_dir
    - Logs: positive count, negative count, balance ratio per label
    """
    # TODO (implementation)
    pass


class CuadToClassification:
    """
    Converts CUAD Q&A samples to clause classification training examples.

    Implements the BaseConverter Protocol.

    Parameters
    ----------
    negative_ratio : float
        Fraction of negative examples to include per clause type.
        Default: 0.5 (equal positive/negative balance).
    max_text_length : int
        Maximum character length for clause text.
        Answers longer than this are truncated with a trailing ellipsis.
    """

    def __init__(
        self,
        negative_ratio: float = 0.5,
        max_text_length: int = 512,
    ) -> None:
        # TODO: load settings, store params
        pass

    def convert(self, samples: list[dict]) -> list[ClauseSample]:
        """
        Convert raw CUAD dicts to ClauseSample list.

        Algorithm
        ---------
        1. For each sample:
            a. Map question → label using QUESTION_TO_LABEL
            b. If answers.text is non-empty:
                → Create positive ClauseSample (is_present=True)
                   text = answers.text[0] (first answer, usually the best)
            c. If answers.text is empty:
                → Create negative ClauseSample (is_present=False) with probability=negative_ratio
                   text = context[:max_text_length] (partial context)
        2. Shuffle the combined list (using cuad_random_seed for reproducibility)
        3. Return all ClauseSamples

        Parameters
        ----------
        samples : list[dict]

        Returns
        -------
        list[ClauseSample]

        Raises
        ------
        ConversionError
            If > 5% of samples fail to convert.
        """
        # TODO (implementation)
        pass

    def get_label_set(self) -> set[str]:
        """Return all EntityLabel values produced by this converter."""
        # Reuse the same mapping from cuad_to_ner to avoid duplication
        from data_processing.cuad_to_ner import QUESTION_TO_LABEL
        return set(QUESTION_TO_LABEL.values())

    def _write_json(self, samples: list[ClauseSample], path: Path) -> None:
        """
        Serialise ClauseSample list to a JSON file.

        Parameters
        ----------
        samples : list[ClauseSample]
        path : Path
            Output file path (will be created/overwritten).

        IMPLEMENTATION NOTES
        --------------------
        - Convert each ClauseSample dataclass to dict via dataclasses.asdict()
        - Use json.dump(data, f, indent=2, ensure_ascii=False)
        - Log: "clause_json_written path=... samples=N"
        """
        # TODO (implementation)
        pass
