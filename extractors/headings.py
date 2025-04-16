import re
from collections import defaultdict
from typing import List, Tuple

import fitz
from collections import defaultdict

from helper_functions.helper_functions import clean_text


def extract_headings_from_document(doc, font_size_threshold=14) -> List[str]:
    headings = []

    # Skip the first page (TOC), so start from the second page (index 1)
    for page_num, page in enumerate(doc[1:], start=2):  # Starts from page 2
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                if not line["spans"]:
                    continue
                text = ''.join([span["text"] for span in line["spans"]]).strip()
                font_size = line["spans"][0]["size"]
                is_bold = "bold" in line["spans"][0]["font"].lower()

                # Clean the text by removing zero-width spaces and other unwanted invisible characters
                cleaned_text = clean_text(text)

                # Check if the text is bold, has a font size >= threshold, and is not empty or just spaces
                if (font_size >= font_size_threshold and is_bold) and cleaned_text:
                    headings.append(cleaned_text)  # Only store the text, no page number

    return headings


def extract_headings_from_document_with_page_number(doc, font_size_threshold=14) -> List[Tuple[str, int]]:
    headings = []

    # Skip the first page (TOC), so start from the second page (index 1)
    for page_num, page in enumerate(doc[1:], start=2):  # Starts from page 2
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                if not line["spans"]:
                    continue
                text = ''.join([span["text"] for span in line["spans"]]).strip()
                font_size = line["spans"][0]["size"]
                is_bold = "bold" in line["spans"][0]["font"].lower()

                # Clean the text by removing zero-width spaces and other unwanted invisible characters
                cleaned_text = clean_text(text)

                # Check if the text is bold, has a font size >= threshold, and is not empty or just spaces
                if (font_size >= font_size_threshold and is_bold) and cleaned_text:
                    headings.append((cleaned_text, page_num))

    return headings


def extract_headings_in_main_text(doc, font_size_threshold=14) -> List[str]:
    headings = extract_headings_from_document(doc, font_size_threshold)

    # Filter headings that start with a number and are not sub-headings
    main_text_headings = [
        heading for heading in headings if re.match(r"^\d+(\.|\s)", heading) and not re.match(r"^\d+\.\d+", heading)
    ]

    return main_text_headings


def extract_heading_number(heading):
    # Extract the heading number (e.g., "1", "1.1", "1.2") from the heading
    match = re.match(r"^\d+(\.\d+)*", heading)
    return match.group(0) if match else ""


def extract_heading_by_name(doc, target_heading):
    # Normalize target heading
    normalized_target = target_heading.lower().strip()

    headings_with_pages = extract_headings_from_document_with_page_number(doc)

    for heading_text, page_num in headings_with_pages:
        if normalized_target in heading_text.lower():
            return page_num, heading_text

    return None, None