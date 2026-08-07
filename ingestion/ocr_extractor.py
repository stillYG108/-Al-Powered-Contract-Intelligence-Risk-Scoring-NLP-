"""
ocr_extractor.py

Scanned PDF OCR pipeline.

Responsibilities:
- Convert PDF pages into images using pdf2image
- Improve image quality using OpenCV
- Extract text using Tesseract OCR
- Return page-wise OCR text

Pipeline:

PDF
 |
 ▼
pdf2image (300 DPI)
 |
 ▼
OpenCV preprocessing
 |
 ▼
Tesseract OCR
 |
 ▼
Combined document text

"""


from pathlib import Path

import cv2
import numpy as np
import pytesseract

from pdf2image import convert_from_path
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

class OCRResult:

    def __init__(
        self,
        text,
        pages,
        metadata
    ):

        self.text = text
        self.pages = pages
        self.metadata = metadata



class OcrExtractor:


    OCR_CONFIG = "--oem 3 --psm 6"



    def extract(
        self,
        pdf_path,
        pages=None
    ):

        """
        Extract text from scanned PDF.

        Parameters
        ----------
        pdf_path:
            PDF file path

        pages:
            List of page numbers to OCR.
            Example:
            [2,5,7]

            If None:
            OCR entire PDF

        """

        pdf_path = Path(pdf_path)


        if not pdf_path.exists():

            raise FileNotFoundError(
                "PDF file not found"
            )


        # Convert PDF pages to images

        images = convert_from_path(

            pdf_path,

            dpi=300,

            poppler_path=r"C:\Users\Sujal  Jethwa\Downloads\Release-26.02.0-0\poppler-26.02.0\Library\bin"

        )
        print(len(images), "images converted from pdf")


        extracted_pages = []


        full_text = ""



        for index, image in enumerate(images):


            page_number = index + 1



            # OCR only selected pages

            if pages and page_number not in pages:

                continue



            print(
                f"OCR processing page {page_number}"
            )


            processed_image = (
                self.preprocess_image(
                    image
                )
            )


            text = pytesseract.image_to_string(

                processed_image,

                config=self.OCR_CONFIG

            )


            text = text.strip()



            page_output = (

                f"\n\n--- PAGE {page_number} ---\n\n"

                + text

            )



            extracted_pages.append(

                {
                    "page": page_number,
                    "text": text
                }

            )


            full_text += page_output



        metadata = {


            "file_name":
                pdf_path.name,


            "pages_processed":
                len(extracted_pages),


            "ocr_engine":
                "tesseract",


            "dpi":
                300,


            "config":
                self.OCR_CONFIG


        }



        return OCRResult(

            text=full_text,

            pages=extracted_pages,

            metadata=metadata

        )



    def preprocess_image(
        self,
        image
    ):

        """
        Image preprocessing pipeline:

        1. RGB -> Grayscale
        2. Adaptive thresholding
        3. Deskew using Tesseract OSD
        4. Noise removal

        """


        # PIL Image -> OpenCV

        img = np.array(image)



        # RGB -> Gray

        gray = cv2.cvtColor(

            img,

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



        # Deskew

        rotated = self.correct_skew(

            threshold

        )



        # Remove noise

        denoised = cv2.medianBlur(

            rotated,

            3

        )


        return denoised



    def correct_skew(
        self,
        image
    ):

        """
        Deskew image using Tesseract OSD.

        """

        try:

            osd = pytesseract.image_to_osd(

                image

            )


            rotation = 0


            for line in osd.split("\n"):


                if "Rotate" in line:

                    rotation = int(

                        line.split(":")[1]

                        .strip()

                    )



            if rotation == 90:

                image = cv2.rotate(

                    image,

                    cv2.ROTATE_90_CLOCKWISE

                )


            elif rotation == 180:

                image = cv2.rotate(

                    image,

                    cv2.ROTATE_180

                )


            elif rotation == 270:

                image = cv2.rotate(

                    image,

                    cv2.ROTATE_90_COUNTERCLOCKWISE

                )



        except Exception:

            # If OSD fails,
            # continue without rotation

            pass



        return image

ocr = OcrExtractor()


try:

    result = ocr.extract(
        "contract.pdf"
    )


    print("OCR Successful")

    print("----------------")

    print(result.metadata)


    print("\nOCR Text:")

    print(result.text[:10000])


except Exception as e:

    print("OCR Error:")

    print(type(e).__name__)

    print(e)