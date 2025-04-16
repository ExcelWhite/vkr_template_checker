def extract_page_sizes(doc):
    return [(
        round(page.rect.width * 25.4 / 72, 2),  # Convert points to mm
        round(page.rect.height * 25.4 / 72, 2)
    ) for page in doc]