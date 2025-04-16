import re

from extractors.headings import extract_headings_in_main_text, extract_heading_number
from extractors.tables import extract_tables_from_document


def check_tables(doc):
    result = {}

    # Extract tables and their captions
    tables = extract_tables_from_document(doc)

    # Extract headings from the main text
    headings = extract_headings_in_main_text(doc)

    # Create a dictionary of heading -> number
    heading_numbers = {heading: extract_heading_number(heading) for heading in headings}

    # Track counters for multiple tables under each heading
    table_counters = {number: 1 for number in heading_numbers.values()}

    for idx, table in enumerate(tables):
        caption = table['caption']

        # Match the table number format
        match = re.match(r"^Таблица (\d+(\.\d+)*)", caption)

        if match:
            table_number = match.group(1)

            for heading, heading_number in heading_numbers.items():
                if table_number.startswith(heading_number):
                    expected_caption = caption  # Assume it's already valid

                    # Only change if table number does *not* start with heading number
                    if not table_number == heading_number:
                        expected_caption = f"Таблица {heading_number}.{table_counters[heading_number]} – {caption.split('–', 1)[-1].strip()}"
                        table_counters[heading_number] += 1
                    else:
                        # Caption is correct if it’s "Таблица {heading_number} – ..."
                        expected_caption = f"Таблица {heading_number} – {caption.split('–', 1)[-1].strip()}"

                    if caption != expected_caption:
                        result["Error"] = f"❌ {caption} should be numbered as {expected_caption}"
                    break
        else:
            result["Error"] = f"❌ {caption} is not correctly formatted"

    if not result:
        return {"Tables Check": "✅ Pass: All tables are correctly numbered"}

    return result
