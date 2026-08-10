from pathlib import Path

from ingestion.pdf_extractor import PdfExtractor
from ingestion.ocr_extractor import OcrExtractor
from ingestion.docx_extractor import DocxExtractor
from ingestion.text_cleaner import TextCleaner


class DocumentRouter:

    def __init__(self):

        self.pdf_extractor = (
            PdfExtractor()
        )

        self.ocr_extractor = (
            OcrExtractor()
        )

        self.docx_extractor = (
            DocxExtractor()
        )

        self.cleaner = (
            TextCleaner()
        )

    def route(self, file_path):

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        extension = (
            file_path.suffix.lower()
        )

        # ==================================
        # PDF
        # ==================================

        if extension == ".pdf":

            return self.process_pdf(
                file_path
            )

        # ==================================
        # DOCX
        # ==================================

        elif extension == ".docx":

            result = (
                self.docx_extractor.extract(
                    file_path
                )
            )

            cleaned = self.cleaner.clean(
                result["text"],
                extraction_method="docx"
            )

            return cleaned

        else:

            raise ValueError(
                f"Unsupported file type: "
                f"{extension}"
            )

    def process_pdf(self, file_path):

        print("\n==============================")
        print("PDF EXTRACTION")
        print("==============================")

        # ----------------------------------
        # Step 1
        # Digital PDF extraction
        # ----------------------------------

        pdf_result = (
            self.pdf_extractor.extract(
                file_path
            )
        )

        flagged = (
            pdf_result["flagged_pages"]
        )

        print(
            "\nFlagged pages:",
            flagged
        )

        # ----------------------------------
        # Step 2
        # OCR flagged pages
        # ----------------------------------

        final_pages = list(
            pdf_result["pages"]
        )

        method = "pdfminer"

        if flagged:

            print(
                "\nSending flagged pages "
                "to OCR..."
            )

            ocr_result = (
                self.ocr_extractor.extract(
                    file_path,
                    pages=flagged
                )
            )

            # Replace PDF text
            # with OCR text
            for item in ocr_result["pages"]:

                page_number = (
                    item["page"]
                )

                index = page_number - 1

                if (
                    0 <= index
                    < len(final_pages)
                ):

                    final_pages[index] = (
                        item["text"]
                    )

            method = "pdfminer+ocr"

        # ----------------------------------
        # Step 3
        # Reassemble
        # ----------------------------------

        final_text = "\n\n".join(
            final_pages
        )

        # ----------------------------------
        # Step 4
        # Clean
        # ----------------------------------

        result = self.cleaner.clean(
            final_text,
            pages=final_pages,
            extraction_method=method
        )

        return result