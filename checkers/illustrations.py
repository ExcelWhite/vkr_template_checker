import re

from extractors.headings import extract_heading_number, extract_headings_in_main_text
from extractors.illustrations import extract_illustrations_from_document


def check_illustrations(doc):
    result = {}

    # Extract illustrations and captions
    illustrations = extract_illustrations_from_document(doc)
    print(illustrations)

    # Extract headings from the main text
    headings = extract_headings_in_main_text(doc)

    # Keep track of the expected numbering based on the headings
    heading_numbers = {}
    for heading in headings:
        # Extract the heading number (e.g., "1", "1.1", "1.2", etc.)
        heading_number = extract_heading_number(heading)
        heading_numbers[heading] = heading_number

    # Check each illustration
    for idx, illustration in enumerate(illustrations):
        caption = illustration['caption']
        # Match the caption format: "Рисунок x.x"
        match = re.match(r"^Рисунок (\d+(\.\d+)*)", caption)

        if match:
            illustration_number = match.group(1)  # Extract the numbering part
            # Find the corresponding heading for this illustration
            for heading, heading_number in heading_numbers.items():
                # Check if illustration number starts with the heading number
                if illustration_number.startswith(heading_number):
                    expected_caption = caption  # The caption is correct, no change needed
                else:
                    expected_caption = f"Рисунок {heading_number}.{idx + 1} {caption.split(maxsplit=1)[-1]}"

                # If the caption doesn't match the expected format
                if caption != expected_caption:
                    result["Error"] = f"❌ {caption} should be numbered as {expected_caption}"
        else:
            result["Error"] = f"❌ {caption} is not correctly formatted"

    if not result:
        return {"Illustrations Check": "✅ Pass: All illustrations are correctly numbered"}

    return result
