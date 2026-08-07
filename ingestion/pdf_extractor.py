
from pathlib import Path

from pdfminer.high_level import extract_text
from pdfminer.pdfpage import PDFPage

from io import BytesIO


class PDFExtractionResult:

    def __init__(
        self,
        text,
        page_text,
        scanned_pages,
        metadata
    ):
        self.text = text
        self.page_text = page_text
        self.scanned_pages = scanned_pages
        self.metadata = metadata


class PdfExtractor:


    # Minimum characters expected from a digital page
    CHAR_THRESHOLD = 50


    def can_handle(self, file_path):

        """
        Check whether this extractor supports the file.
        """

        return Path(file_path).suffix.lower() == ".pdf"



    def extract(self, file_path):

        """
        Extract text from PDF page-by-page.

        Returns:
        - Complete extracted text
        - Individual page text
        - Pages requiring OCR
        """

        pdf_path = Path(file_path)


        if not pdf_path.exists():

            raise FileNotFoundError(
                "PDF file not found"
            )


        pages_text = []

        scanned_pages = []


        # Count total pages

        with open(pdf_path, "rb") as file:

            total_pages = sum(
                1 for _ in PDFPage.get_pages(file)
            )



        # Extract every page separately

        for page_number in range(total_pages):


            page_text = extract_text(
                str(pdf_path),
                page_numbers=[page_number]
            )


            if page_text is None:

                page_text = ""


            page_text = page_text.strip()


            pages_text.append(page_text)



            # Detect scanned pages

            if len(page_text) < self.CHAR_THRESHOLD:

                scanned_pages.append(
                    page_number + 1
                )



        # Combine all pages

        full_text = "\n\n".join(
            pages_text
        )



        metadata = {

            "file_name": pdf_path.name,

            "total_pages": total_pages,

            "extracted_characters": len(full_text),

            "scanned_page_count":
                len(scanned_pages)

        }



        return PDFExtractionResult(

            text=full_text,

            page_text=pages_text,

            scanned_pages=scanned_pages,

            metadata=metadata

        )

pdf = PdfExtractor()

try:

    result = pdf.extract("contract.pdf")

    print("PDF Extraction Successful")

    print("----------------------")

    print("Total Pages:")
    print(result.metadata["total_pages"])

    print("\nScanned Pages:")
    print(result.scanned_pages)

    print("\nExtracted Text Sample:")
    print(result.text[:10000])


except Exception as e:

    print("PDF Extractor Error:")
    print(type(e).__name__)
    print(e)
