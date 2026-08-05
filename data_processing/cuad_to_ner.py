"""
data_processing/cuad_to_ner.py
===============================
Converts CUAD Q&A annotations into spaCy NER training data.

PURPOSE
-------
Transforms raw CUAD samples (Q&A format) into spaCy-compatible NER
training examples stored as a DocBin binary file.

OUTPUT FORMAT
-------------
Two spaCy DocBin files:
    data/processed/cuad_ner_train.spacy
    data/processed/cuad_ner_dev.spacy

Each DocBin contains spaCy Doc objects with .ents set.
These are loaded directly by `spacy train` via the training config.

MAPPING STRATEGY: CUAD Q → EntityLabel
----------------------------------------
CUAD question text is matched to an EntityLabel via the question-to-label
lookup table (QUESTION_TO_LABEL dict below).

Each CUAD question template contains a unique phrase (e.g.,
"Highlight the parts...related to parties" → EntityLabel.PARTIES).

All 41 CUAD clause types are mapped (Phase 1 decision).
The 4 core NER types (ORG, DATE, MONEY, GPE) are ALSO included by
running spaCy's base model (en_core_web_lg) on each text and adding
those entities to the training set. This gives the model dual training
signal: CUAD-derived labels + pre-existing NER knowledge.

CHUNKING STRATEGY
-----------------
CUAD contexts can be very long (10,000+ chars). spaCy NER works on
chunks of up to max_text_length chars (default: 512).

Chunking algorithm:
    1. Split context at sentence boundaries (using spaCy sentenciser)
    2. Accumulate sentences until chunk size <= max_text_length
    3. Adjust entity offsets to be relative to chunk start
    4. Discard chunks with no entity spans (negative examples configurable)

SPAN ALIGNMENT
--------------
CUAD answer_start offsets are character-based and refer to the FULL context.
After chunking, offsets must be adjusted:
    chunk_start_offset = entity.start - chunk_char_start
    chunk_end_offset   = entity.end   - chunk_char_start

All spans are validated by SpanValidator before being written to DocBin.

NEGATIVE EXAMPLES
-----------------
CUAD includes many "no answer" examples (empty answers.text list).
Strategy: include 1 negative example for every 3 positive examples (ratio=0.33).
This prevents the model from biasing toward always predicting an entity.

IMPLEMENTATION NOTES
--------------------
- Use spacy.blank("en") to create Doc objects (no model needed for DocBin)
- Use doc.set_ents() with spans derived from character offsets
- Use DocBin.add(doc) in a loop, then DocBin.to_disk(path)
- Log progress with tqdm over the sample list
- Log per-label entity counts after conversion (for dataset_stats integration)

USAGE EXAMPLE
-------------
    from data_processing.cuad_to_ner import CuadToNer
    from pathlib import Path

    converter = CuadToNer()
    ner_samples = converter.convert(train_samples)

    # Module-level convenience:
    from data_processing import build_ner_corpus
    build_ner_corpus(train_samples, dev_samples, output_dir=Path("data/processed"))
"""

from __future__ import annotations

from pathlib import Path

from core.exceptions import ConversionError  # noqa: F401
from core.logging import get_logger
from core.types import Entity, EntityLabel, NERSample

log = get_logger(__name__)

# ---------------------------------------------------------------------------
# CUAD question text → EntityLabel mapping
# (all 41 clause types — Phase 1 decision)
# ---------------------------------------------------------------------------
#
# Each key is a UNIQUE substring of the CUAD question template.
# Matching is done with str.lower() + 'key in question.lower()'.
# Keys are ordered from most specific to least specific to avoid
# false matches (e.g., "termination for convenience" before "termination").
#
QUESTION_TO_LABEL: dict[str, str] = {
    "document name":                    EntityLabel.DOCUMENT_NAME.value,
    "parties":                          EntityLabel.PARTIES.value,
    "agreement date":                   EntityLabel.AGREEMENT_DATE.value,
    "effective date":                   EntityLabel.EFFECTIVE_DATE.value,
    "expiration date":                  EntityLabel.EXPIRATION_DATE.value,
    "renewal term":                     EntityLabel.RENEWAL_TERM.value,
    "notice period to terminate":       EntityLabel.NOTICE_PERIOD_TO_TERMINATE.value,
    "governing law":                    EntityLabel.GOVERNING_LAW.value,
    "most favored nation":              EntityLabel.MOST_FAVORED_NATION.value,
    "non-compete":                      EntityLabel.NON_COMPETE.value,
    "exclusivity":                      EntityLabel.EXCLUSIVITY.value,
    "no-solicit of customers":          EntityLabel.NO_SOLICIT_OF_CUSTOMERS.value,
    "no-solicit of employees":          EntityLabel.NO_SOLICIT_OF_EMPLOYEES.value,
    "non-disparagement":                EntityLabel.NON_DISPARAGEMENT.value,
    "termination for convenience":      EntityLabel.TERMINATION_FOR_CONVENIENCE.value,
    "rofr/rofo/rofn":                   EntityLabel.ROFR_ROFO_ROFN.value,
    "change of control":                EntityLabel.CHANGE_OF_CONTROL.value,
    "anti-assignment":                  EntityLabel.ANTI_ASSIGNMENT.value,
    "revenue/profit sharing":           EntityLabel.REVENUE_PROFIT_SHARING.value,
    "price restriction":                EntityLabel.PRICE_RESTRICTION.value,
    "minimum commitment":               EntityLabel.MINIMUM_COMMITMENT.value,
    "volume restriction":               EntityLabel.VOLUME_RESTRICTION.value,
    "ip ownership assignment":          EntityLabel.IP_OWNERSHIP_ASSIGNMENT.value,
    "joint ip ownership":               EntityLabel.JOINT_IP_OWNERSHIP.value,
    "license grant":                    EntityLabel.LICENSE_GRANT.value,
    "non-transferable license":         EntityLabel.NON_TRANSFERABLE_LICENSE.value,
    "affiliate license-licensor":       EntityLabel.AFFILIATE_LICENSE_LICENSOR.value,
    "affiliate license-licensee":       EntityLabel.AFFILIATE_LICENSE_LICENSEE.value,
    "unlimited license":                EntityLabel.UNLIMITED_LICENSE.value,
    "irrevocable or perpetual":         EntityLabel.IRREVOCABLE_OR_PERPETUAL.value,
    "source code escrow":               EntityLabel.SOURCE_CODE_ESCROW.value,
    "post-termination services":        EntityLabel.POST_TERMINATION_SERVICES.value,
    "audit rights":                     EntityLabel.AUDIT_RIGHTS.value,
    "uncapped liability":               EntityLabel.UNCAPPED_LIABILITY.value,
    "cap on liability":                 EntityLabel.CAP_ON_LIABILITY.value,
    "liquidated damages":               EntityLabel.LIQUIDATED_DAMAGES.value,
    "warranty duration":                EntityLabel.WARRANTY_DURATION.value,
    "insurance":                        EntityLabel.INSURANCE.value,
    "covenant not to sue":              EntityLabel.COVENANT_NOT_TO_SUE.value,
    "third party beneficiary":          EntityLabel.THIRD_PARTY_BENEFICIARY.value,
    "limitation of liability":          EntityLabel.LIMITATION_OF_LIABILITY.value,
}


def build_ner_corpus(
    train_samples: list[dict],
    dev_samples: list[dict],
    output_dir: Path,
) -> None:
    """
    Module-level function: convert + write DocBin files to disk.

    Exported from data_processing/__init__.py.

    Parameters
    ----------
    train_samples : list[dict]
        Training split from CuadLoader.load()
    dev_samples : list[dict]
        Dev split from CuadLoader.load()
    output_dir : Path
        Directory where .spacy files will be written.
        Files: {output_dir}/cuad_ner_train.spacy, cuad_ner_dev.spacy

    Side Effects
    ------------
    - Writes two .spacy files to output_dir
    - Logs counts: samples processed, entities found, spans discarded
    """
    # TODO (implementation)
    pass


class CuadToNer:
    """
    Converts CUAD Q&A samples to spaCy NER training examples.

    Implements the BaseConverter Protocol.

    Parameters
    ----------
    max_chunk_length : int
        Maximum character length per NER sample chunk.
        Defaults to settings.max_text_length (512).
    negative_ratio : float
        Fraction of negative (no-entity) examples to include.
        Default: 0.33 (1 negative per 3 positives).
    """

    def __init__(
        self,
        max_chunk_length: int | None = None,
        negative_ratio: float = 0.33,
    ) -> None:
        # TODO: load settings, store params
        pass

    def convert(self, samples: list[dict]) -> list[NERSample]:
        """
        Convert raw CUAD dicts → list of NERSample.

        Algorithm
        ---------
        1. For each sample:
            a. Determine label: _map_question_to_label(sample["question"])
            b. If label is None: skip (unknown question template) + log warning
            c. Extract answer spans from sample["answers"]
            d. Chunk the context into max_chunk_length pieces
            e. For each chunk that overlaps with an answer span:
                → Create Entity with adjusted offsets
                → Run SpanValidator on the chunk's entities
                → Create NERSample
            f. Optionally include negative chunks (no answers) per negative_ratio
        2. Return all NERSamples

        Parameters
        ----------
        samples : list[dict]
            Raw CUAD samples.

        Returns
        -------
        list[NERSample]
            Training examples with validated, non-overlapping entity spans.

        Raises
        ------
        ConversionError
            If > 5% of samples fail to convert (malformed data).
        """
        # TODO (implementation)
        pass

    def get_label_set(self) -> set[str]:
        """Return all EntityLabel values produced by this converter."""
        return set(QUESTION_TO_LABEL.values())

    def _map_question_to_label(self, question: str) -> str | None:
        """
        Map a CUAD question string to an EntityLabel value.

        Uses substring matching (case-insensitive) against QUESTION_TO_LABEL.

        Parameters
        ----------
        question : str
            Full CUAD question text.

        Returns
        -------
        str | None
            EntityLabel.value string, or None if no match found.

        IMPLEMENTATION NOTES
        --------------------
        - Iterate QUESTION_TO_LABEL keys in order (dict is ordered in Python 3.7+)
        - Return first match: if key.lower() in question.lower()
        - Log at DEBUG level if no match (should not happen with correct CUAD version)
        """
        # TODO (implementation)
        pass

    def _chunk_context(self, context: str) -> list[tuple[int, int, str]]:
        """
        Split a long context string into overlapping chunks.

        Parameters
        ----------
        context : str
            Full contract context (can be 10,000+ chars).

        Returns
        -------
        list[tuple[int, int, str]]
            List of (chunk_start, chunk_end, chunk_text) tuples.
            chunk_start and chunk_end are offsets into the ORIGINAL context.

        CHUNKING ALGORITHM
        ------------------
        1. Split context into sentences using spaCy's sentencizer
        2. Greedily accumulate sentences until adding the next would exceed max_chunk_length
        3. Start a new chunk at the next sentence boundary
        4. No overlapping in Phase 1 (overlap adds complexity; revisit in Phase 2)
        """
        # TODO (implementation)
        pass
