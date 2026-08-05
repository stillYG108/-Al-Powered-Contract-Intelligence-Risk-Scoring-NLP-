"""
data_processing/span_validator.py
===================================
Validates and resolves overlapping or misaligned annotation spans.

PURPOSE
-------
CUAD annotations sometimes have spans that:
    1. Overlap each other (two answers cover some of the same text)
    2. Are misaligned (start > end, or offsets exceed text length)
    3. Are empty (start == end)

This module detects and resolves these issues BEFORE they reach spaCy,
which would crash on invalid spans.

RESOLUTION STRATEGY (Phase 1 decision)
---------------------------------------
For OVERLAPPING spans: keep the LONGER span, discard the shorter one.
Rationale: longer spans capture more clause context, which is better
for an NER model learning legal boundaries.

For MISALIGNED spans: discard entirely and emit a warning.
These are data errors in CUAD annotations and cannot be recovered.

For EMPTY spans: discard silently (zero-length entities carry no signal).

AUDIT TRAIL
-----------
Every resolution is recorded as a SpanConflict dataclass and returned
alongside the cleaned entity list. This allows dataset_stats.py to
report how many conflicts were found and resolved.

ALGORITHM: Interval Sweep
--------------------------
For a given list of Entity spans:
1. Sort by start position, then by length (descending) for ties
2. Maintain a "last accepted end" pointer
3. Iterate: if span.start >= last_accepted_end → accept, update pointer
             if span.start <  last_accepted_end → OVERLAP DETECTED
                → compare lengths: keep longer, discard shorter
                → if equal length: keep the one with higher score (or first)
4. Return (cleaned_entities, conflicts)

This is O(n log n) and handles all edge cases including nested spans
and multiple spans overlapping a single long span.

PURE FUNCTION DESIGN
--------------------
validate() is a pure function (no I/O, no state):
    Input:  text (str), entities (list[Entity]), doc_id (str)
    Output: (list[Entity], list[SpanConflict])

This makes it trivially testable with synthetic inputs.

USAGE EXAMPLE
-------------
    from data_processing.span_validator import SpanValidator

    cleaned, conflicts = SpanValidator.validate(
        text=context_text,
        entities=raw_entities,
        doc_id="cuad_contract_001",
    )

    if conflicts:
        for c in conflicts:
            log.warning("span_conflict", **dataclasses.asdict(c))
"""

from __future__ import annotations

from core.exceptions import SpanValidationError  # noqa: F401
from core.logging import get_logger
from core.types import Entity, SpanConflict

log = get_logger(__name__)


class SpanValidator:
    """
    Validates and resolves entity span issues.

    All methods are @staticmethod — no instantiation needed.
    Usage: SpanValidator.validate(text, entities, doc_id)
    """

    @staticmethod
    def validate(
        text: str,
        entities: list[Entity],
        doc_id: str = "",
    ) -> tuple[list[Entity], list[SpanConflict]]:
        """
        Validate and clean a list of entity spans for a given text.

        Performs three checks in order:
        1. Bounds check (remove misaligned / empty spans)
        2. Overlap resolution (keep longer span, discard shorter)
        3. Return clean list + audit records

        Parameters
        ----------
        text : str
            The source text these entities are aligned to.
            Used for bounds checking.
        entities : list[Entity]
            Raw entity spans to validate.
        doc_id : str
            Source document identifier (for SpanConflict audit records).

        Returns
        -------
        tuple[list[Entity], list[SpanConflict]]
            - list[Entity]: validated, non-overlapping, in-bounds entities
            - list[SpanConflict]: audit records for every discarded span

        Raises
        ------
        SpanValidationError
            Only if text is empty and entities are non-empty
            (this indicates a programming error upstream, not a data error).
        """
        # TODO (implementation): bounds check → overlap resolution → return
        pass

    @staticmethod
    def _check_bounds(
        entities: list[Entity],
        text_length: int,
        doc_id: str,
    ) -> tuple[list[Entity], list[SpanConflict]]:
        """
        Remove entities whose offsets are invalid.

        Invalid conditions:
            - start < 0
            - end > text_length
            - start >= end  (empty or inverted span)

        Parameters
        ----------
        entities : list[Entity]
        text_length : int
            len(text) of the source context.
        doc_id : str

        Returns
        -------
        tuple[list[Entity], list[SpanConflict]]
            Valid entities + SpanConflict records for discarded ones.
        """
        # TODO (implementation)
        pass

    @staticmethod
    def _resolve_overlaps(
        entities: list[Entity],
        doc_id: str,
    ) -> tuple[list[Entity], list[SpanConflict]]:
        """
        Resolve overlapping spans using the "keep longer" strategy.

        Uses an interval sweep algorithm (see module docstring).

        Parameters
        ----------
        entities : list[Entity]
            Bounds-checked entities (all start/end are valid).
        doc_id : str

        Returns
        -------
        tuple[list[Entity], list[SpanConflict]]
            Non-overlapping entities + conflict audit records.

        ALGORITHM DETAIL
        ----------------
        Sort by (start ASC, length DESC).
        Maintain accepted list and last_end pointer.
        For each span:
            if span.start >= last_end → accept, update last_end = span.end
            else (overlap):
                accepted_last = accepted[-1]
                if span.end - span.start > accepted_last.end - accepted_last.start:
                    → swap: remove accepted_last, add current span
                    → SpanConflict(kept=current, discarded=accepted_last)
                else:
                    → discard current
                    → SpanConflict(kept=accepted_last, discarded=current)
        """
        # TODO (implementation)
        pass
