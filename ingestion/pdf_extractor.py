from pathlib import Path

from pdfminer.high_level import extract_text
from pdfminer.pdfpage import PDFPage


class PdfExtractor:

    CHAR_THRESHOLD = 50

    def extract(self, pdf_file):

        pdf_file = Path(pdf_file)

        if not pdf_file.exists():
            raise FileNotFoundError(
                f"PDF not found: {pdf_file}"
            )

        if pdf_file.suffix.lower() != ".pdf":
            raise ValueError(
                "Only PDF files are supported."
            )

        # Count pages
        with open(
            pdf_file,
            "rb"
        ) as file:

            total_pages = sum(
                1
                for _ in PDFPage.get_pages(file)
            )

        page_texts = []
        flagged_pages = []

        # Extract page-by-page
        for page_index in range(
            total_pages
        ):

            text = extract_text(
                str(pdf_file),
                page_numbers=[page_index]
            )

            if text is None:
                text = ""

            text = text.strip()

            page_number = page_index + 1

            page_texts.append(text)

            print(
                f"PDF page {page_number}: "
                f"{len(text)} characters"
            )

            # Scanned-page detection
            if len(text) < self.CHAR_THRESHOLD:

                flagged_pages.append(
                    page_number
                )

        full_text = "\n\n".join(
            page_texts
        )

        return {
            "text": full_text,
            "pages": page_texts,
            "flagged_pages": flagged_pages,
            "metadata": {
                "file_name": pdf_file.name,
                "pages": total_pages,
                "extraction_method": "pdfminer",
                "threshold": self.CHAR_THRESHOLD
            }
        }