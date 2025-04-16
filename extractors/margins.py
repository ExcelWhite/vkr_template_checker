def extract_margins(doc):
    """Extract margins from the PDF document."""
    margins = []
    for page in doc:
        # Get the page dimensions
        rect = page.rect
        # Get the text bounding box
        text_instances = page.search_for("")  # Search for all text
        if text_instances:
            # Assuming the first text instance gives us the bounding box
            text_rect = text_instances[0]
            left_margin = text_rect.x0  # Distance from the left edge of the page
            right_margin = rect.width - text_rect.x1  # Distance from the right edge of the page
            top_margin = text_rect.y0  # Distance from the top edge of the page
            bottom_margin = rect.height - text_rect.y1  # Distance from the bottom edge of the page
        else:
            # If no text is found, assume full margins
            left_margin = rect.width
            right_margin = rect.width
            top_margin = rect.height
            bottom_margin = rect.height

        margins.append((left_margin, right_margin, top_margin, bottom_margin))

        # Debugging: Print margins for each page
        # print(
        #     f"Left Margin: {left_margin}mm, Right Margin: {right_margin}mm, Top Margin: {top_margin}mm, Bottom Margin: {bottom_margin}mm")

    return margins
