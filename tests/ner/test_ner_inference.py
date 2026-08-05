"""
tests/ner/test_ner_inference.py
================================
Unit and integration tests for ner/inference.py — NERModel class.

WHAT IS TESTED
--------------
1. load_model()
   - Raises ModelNotFoundError if path does not exist
   - Returns NERModel instance on valid path
   - Returns same instance on second call (singleton cache)

2. NERModel.extract_entities()
   - Returns list[Entity] for standard contract text
   - Returns [] for empty string input (no crash)
   - Entity offsets are within text bounds
   - Entities are non-overlapping (invariant)
   - Entities are sorted by start position

3. NERModel.batch_extract()
   - Result length == input length
   - Consistent with calling extract_entities() one-at-a-time
   - Handles empty string in batch without crashing

4. NERModel.model_info()
   - Returns dict with "model_path", "labels", "loaded_at" keys
   - "labels" is a non-empty list

5. _to_entity() helper
   - Pure function: creates Entity with correct label, text, start, end
   - offset parameter correctly shifts start/end

TEST STRATEGY
-------------
- With real model: use @pytest.mark.integration — load models/ner_baseline
  (skip if model not on disk)
- Without real model: mock spaCy nlp object → unit test NERModel logic
  in isolation from spaCy internals

SKIPPING
--------
    pytestmark = pytest.mark.skipif(
        not Path("models/ner_baseline").exists(),
        reason="Trained model not found — run scripts/train_ner.sh first"
    )
"""

from __future__ import annotations

from pathlib import Path

import pytest

# TODO (implementation): from ner.inference import NERModel, load_model, _to_entity
# from ner.base import BaseNERModel
# from core.types import Entity

pytestmark = pytest.mark.skipif(
    not Path("models/ner_baseline").exists(),
    reason="Trained model not found — run scripts/train_ner.sh first",
)


class TestLoadModel:
    """Tests for the load_model() singleton function."""

    def test_raises_model_not_found_for_bad_path(self, tmp_path):
        """load_model() raises ModelNotFoundError for non-existent path."""
        pass

    def test_returns_ner_model_instance(self):
        """load_model() returns a NERModel (or BaseNERModel-compatible) instance."""
        pass

    def test_singleton_returns_same_instance(self):
        """Calling load_model() twice returns the same object (cached)."""
        pass


class TestExtractEntities:
    """Tests for NERModel.extract_entities()."""

    def test_returns_list_of_entities(self):
        """Standard contract text produces a non-empty list."""
        pass

    def test_empty_input_returns_empty_list(self):
        """Empty string input → [] (no exception)."""
        pass

    def test_entity_offsets_within_text_bounds(self):
        """All entity start < end <= len(text)."""
        pass

    def test_entities_are_sorted_by_start(self):
        """Returned entities are sorted by start character position."""
        pass

    def test_entities_are_non_overlapping(self):
        """No two returned entities overlap in character position."""
        pass


class TestBatchExtract:
    """Tests for NERModel.batch_extract()."""

    def test_result_length_matches_input_length(self):
        """len(result) == len(input texts)."""
        pass

    def test_handles_empty_string_in_batch(self):
        """Empty string in batch → [] for that index, no crash."""
        pass


class TestToEntityHelper:
    """Tests for _to_entity() pure helper function."""

    def test_creates_entity_with_correct_fields(self):
        """_to_entity converts a spaCy span to Entity with correct attrs."""
        pass

    def test_offset_shifts_start_and_end(self):
        """offset parameter adds to both start_char and end_char."""
        pass
