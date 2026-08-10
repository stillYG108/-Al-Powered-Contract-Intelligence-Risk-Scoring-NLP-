from pathlib import Path

import cv2
import numpy as np
import pytesseract
from pdf2image import convert_from_path

# TESSERACT

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# POPPLER

POPPLER_PATH = (r"C:\Program Files\Release-26.02.0-0\poppler-26.02.0\Library\bin")


# OCR EXTRACTOR

class OcrExtractor:

    OCR_CONFIG = "--oem 3 --psm 6"

    def extract(self, pdf_file, pages=None):

        pdf_file = Path(pdf_file)

        if not pdf_file.exists():
            raise FileNotFoundError(
                f"PDF not found: {pdf_file}"
            )

        if pdf_file.suffix.lower() != ".pdf":
            raise ValueError(
                "Only PDF files are supported."
            )

        print(
            f"\nOCR file: {pdf_file.name}"
        )

        images = convert_from_path(
            str(pdf_file),
            dpi=300,
            poppler_path=POPPLER_PATH
        )

        print(
            f"Converted {len(images)} page(s)"
        )

        extracted_pages = []

        for number, image in enumerate(
            images,
            start=1
        ):

            # If router supplied specific pages
            if pages is not None:
                if number not in pages:
                    continue

            print(
                f"OCR processing page {number}"
            )

            processed = (
                self.preprocess_image(image)
            )

            text = pytesseract.image_to_string(
                processed,
                config=self.OCR_CONFIG
            )

            text = text.strip()

            extracted_pages.append({
                "page": number,
                "text": text
            })

        # Reassemble pages
        page_texts = []

        for page in extracted_pages:

            page_texts.append(
                f"--- PAGE {page['page']} ---\n"
                f"{page['text']}"
            )

        full_text = "\n\n".join(
            page_texts
        )

        return {
            "text": full_text,
            "pages": extracted_pages,
            "metadata": {
                "file_name": pdf_file.name,
                "pages_processed": len(
                    extracted_pages
                ),
                "extraction_method": "ocr",
                "ocr_engine": "tesseract",
                "dpi": 300,
                "config": self.OCR_CONFIG
            }
        }

    # PREPROCESSING

    def preprocess_image(self, image):

        # PIL -> NumPy
        image = np.array(image)

        # RGB -> grayscale
        gray = cv2.cvtColor(
            image,
            cv2.COLOR_RGB2GRAY
        )

        # Adaptive threshold
        threshold = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            11
        )

        # Denoising
        cleaned = cv2.medianBlur(
            threshold,
            3
        )

        return cleaned