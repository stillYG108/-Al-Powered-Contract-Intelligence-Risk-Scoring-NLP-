"""
ingestion/docx_extractor.py
============================
Text extractor for Microsoft Word (.docx) files.

PURPOSE
-------
Extracts all readable text from .docx documents using python-docx.
Handles paragraphs, tables, headers/footers, and inline text runs.

WHEN THIS EXTRACTOR IS CHOSEN
------------------------------
DocumentRouter calls can_handle() → True for .docx extension.
This extractor is always definitive for .docx (no auto-detect needed).

LIBRARY: python-docx
--------------------
python-docx reads the OOXML format (zip of XML files) natively.
It gives access to Document.paragraphs, Document.tables, and sections.

WHAT IS EXTRACTED (in reading order)
-------------------------------------
1. Document body paragraphs  (most content)
2. Table cells  (row by row, cell by cell, joined with " | ")
3. Headers and footers from each section  (often contain doc title / date)
4. Text boxes (shapes) are NOT extracted — too complex for Phase 1

TEXT STITCHING STRATEGY
------------------------
    [HEADER] {header text}
    
    {paragraph 1}
    {paragraph 2}
    
    [TABLE]
    {row1_col1} | {row1_col2} | {row1_col3}
    {row2_col1} | {row2_col2} | {row2_col3}
    
    [FOOTER] {footer text}

Rationale: preserves structure visible to a human reader while remaining
clean enough for NER. TextCleaner handles whitespace normalisation.

METADATA INCLUDED IN RESULT
----------------------------
{
    "author": "Jane Smith",
    "last_modified_by": "John Doe",
    "created": "2024-01-15T09:00:00",
    "modified": "2024-03-20T14:30:00",
    "paragraph_count": 152,
    "table_count": 3,
    "word_count": 8421
}

IMPLEMENTATION NOTES
--------------------
- Preserve paragraph style names for Phase 2 (heading detection)
- Skip empty paragraphs (len(para.text.strip()) == 0)
- python-docx does not handle .doc (binary format) — raise ExtractionError
  with a clear message directing user to convert to .docx first

USAGE EXAMPLE
-------------
    from ingestion.docx_extractor import DocxExtractor
    from pathlib import Path

    extractor = DocxExtractor()
    result = extractor.extract(Path("contract.docx"))
    print(result.metadata["table_count"])
"""

from __future__ import annotations

from pathlib import Path

from core.exceptions import ExtractionError  # noqa: F401
from core.logging import get_logger
from core.types import ExtractionMethod, ExtractionResult

log = get_logger(__name__)


class DocxExtractor:
    """
    Extracts text from .docx files using python-docx.

    Implements the BaseExtractor Protocol.

    THREAD SAFETY
    -------------
    Stateless — safe to share across threads. python-docx Document
    objects are created per extract() call and not stored as instance state.
    """

    SUPPORTED_EXTENSIONS: frozenset[str] = frozenset({".docx"})

    def can_handle(self, path: Path) -> bool:
        """
        Return True for .docx files only (NOT .doc binary format).

        Parameters
        ----------
        path : Path

        Returns
        -------
        bool
        """
        # TODO: return path.suffix.lower() in self.SUPPORTED_EXTENSIONS
        pass

    def extract(self, path: Path) -> ExtractionResult:
        """
        Extract text from a .docx file in reading order.

        Algorithm
        ---------
        1. Load document: docx.Document(path)
        2. Extract core properties (author, dates) from document.core_properties
        3. Iterate document.paragraphs → collect non-empty paragraph texts
        4. Iterate document.tables:
            a. For each row: join cell texts with " | "
            b. Prefix table block with "[TABLE]\n"
        5. Iterate document.sections:
            a. Extract header and footer text if present
        6. Concatenate all parts with appropriate spacing
        7. Compute word_count from resulting text
        8. Return ExtractionResult

        Parameters
        ----------
        path : Path
            Path to the .docx file.

        Returns
        -------
        ExtractionResult
            raw_text: full document text with structural markers
            method: ExtractionMethod.DOCX_PARSE
            page_count: -1 (python-docx does not expose page count)
            metadata: {author, last_modified_by, created, modified,
                        paragraph_count, table_count, word_count}

        Raises
        ------
        ExtractionError
            - If path does not exist
            - If file is .doc (binary) not .docx (raise with helpful message)
            - If docx.Document() raises BadZipFile (file is corrupted)
        """
        # TODO (implementation): python-docx extraction logic
        pass

    def _extract_table_text(self, table) -> str:
        """
        Convert a python-docx Table into a pipe-delimited string block.

        Format:
            [TABLE]
            Cell(0,0) | Cell(0,1) | Cell(0,2)
            Cell(1,0) | Cell(1,1) | Cell(1,2)

        Parameters
        ----------
        table : docx.table.Table
            A python-docx Table object.

        Returns
        -------
        str
            Formatted table text block.

        TESTING NOTE
        ------------
        Pure function of a table object → easy to unit test with mock tables.
        """
        # TODO (implementation)
        pass
