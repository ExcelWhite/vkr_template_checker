import re
import fitz  # PyMuPDF

from helper_functions.helper_functions import is_valid_page_number, is_sequential


def check_page_numeration(doc):
    page_numbers = []
    num_pages = doc.page_count

    # Iterate through each page in the document (page numbering starts from 1)
    for page_num in range(num_pages):
        page = doc.load_page(page_num)
        text = page.get_text("text")

        # Split the text into lines
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        # Get the last line on the page
        last_line = lines[-1].strip()

        # Adjust page number to account for 0-based index
        expected_page_number = page_num + 1

        # Check if the last line contains a valid Arabic numeral and matches the expected page number
        if is_valid_page_number(last_line, expected_page_number):
            page_numbers.append(int(last_line))
        else:
            return {"Page Number Error": f"Invalid page number on page {expected_page_number}: {last_line}"}

    # Check if the page numbers are sequential
    if not is_sequential(page_numbers):
        return {"Page Number Error": "Page numbers are not sequential"}

    return {"Page Numeration Check": "✅ Pass: Page numbers are correct and sequential"}

