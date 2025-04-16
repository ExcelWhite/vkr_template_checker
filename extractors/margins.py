def extract_margins(doc):
    """Extract margins from the PDF document."""
    margins = []  # List to hold margins for each page

    for page in doc:
        # Get the page dimensions
        rect = page.rect

        # Get the text bounding boxes
        text_blocks = page.get_text("dict")["blocks"]

        # Initialize variables for margins for the current page
        left_margin = rect.width
        right_margin = rect.width
        top_margin = rect.height
        bottom_margin = rect.height

        # Iterate through text blocks to find the first non-empty text block
        for block in text_blocks:
            if "lines" in block:  # Ensure it's a text block
                for line in block["lines"]:
                    if line["spans"]:  # Check if there are spans (text)
                        # Get the bounding box of the first span
                        text_rect = line["spans"][0]["bbox"]
                        left_margin = min(left_margin, text_rect[0])  # Update left margin
                        right_margin = min(right_margin, rect.width - text_rect[2])  # Update right margin
                        top_margin = min(top_margin, text_rect[1])  # Update top margin
                        bottom_margin = min(bottom_margin, rect.height - text_rect[3])  # Update bottom margin
                        break  # Exit after processing the first non-empty line

        # Append the margins for the current page to the list
        margins.append((left_margin, right_margin, top_margin, bottom_margin))
    # Return the margins for all pages
    return margins
