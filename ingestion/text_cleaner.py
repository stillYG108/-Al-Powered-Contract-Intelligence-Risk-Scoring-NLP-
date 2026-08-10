import re
import unicodedata


class TextCleaner:

    LIGATURES = {
        "ﬁ": "fi",
        "ﬂ": "fl",
        "ﬃ": "ffi",
        "ﬄ": "ffl",
        "ﬅ": "st",
        "ﬆ": "st"
    }

    def clean(
        self,
        text,
        pages=None,
        extraction_method="unknown"
    ):

        if not text:
            return {
                "text": "",
                "metadata": {
                    "pages": 0,
                    "word_count": 0,
                    "extraction_method":
                        extraction_method
                }
            }

        # Unicode normalization

        text = unicodedata.normalize(
            "NFKC",
            text
        )

        # Ligatures

        for old, new in self.LIGATURES.items():

            text = text.replace(
                old,
                new
            )

        # Whitespace

        text = text.replace(
            "\r\n",
            "\n"
        )

        text = text.replace(
            "\r",
            "\n"
        )

        text = re.sub(
            r"[ \t]+",
            " ",
            text
        )

        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text
        )

        # Remove empty lines at edges

        text = text.strip()

        # Header/footer detection

        if pages and len(pages) > 1:

            repeated = (
                self.find_repeated_lines(
                    pages
                )
            )

            lines = []

            for line in text.splitlines():

                if line.strip() not in repeated:
                    lines.append(line)

            text = "\n".join(lines)

        # Metadata

        metadata = {
            "pages": (
                len(pages)
                if pages
                else 1
            ),
            "word_count": len(
                text.split()
            ),
            "extraction_method":
                extraction_method
        }

        return {
            "text": text,
            "metadata": metadata
        }

    def find_repeated_lines(
        self,
        pages
    ):

        page_sets = []

        for page in pages:

            lines = set()

            for line in page.splitlines():

                line = line.strip()

                if (
                    line
                    and len(line) < 60
                ):
                    lines.add(line)

            page_sets.append(lines)

        if not page_sets:
            return set()

        # Must appear on every page
        return set.intersection(
            *page_sets
        )