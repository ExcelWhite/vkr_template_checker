import re


def estimate_line_spacing(page):
    spacings = []
    previous_y = None
    lines = []

    blocks = page.get_text("dict")["blocks"]
    for block in blocks:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            y = line["bbox"][1]  # Top Y coordinate
            if previous_y is not None:
                spacing = abs(y - previous_y)
                spacings.append(spacing)
            previous_y = y
    return spacings


def normalize_title(title):
    return re.sub(r"\s+", " ", title.strip().lower())


def compare_toc_and_headings(toc_entries, headings):
    # Normalize and convert TOC entries into a set
    toc_set = set((normalize_title(title), page) for title, page in toc_entries)

    # Normalize and convert headings into a set
    actual_set = set((normalize_title(title), page) for title, page in headings)

    # Find missing and extra entries
    missing = toc_set - actual_set
    extra = actual_set - toc_set

    return missing, extra


def clean_text(text: str) -> str:
    # Remove zero-width space and any other similar invisible characters
    return text.replace("\u200b", "").strip()


def is_valid_page_number(last_line, expected_page_number):
    # Check if the last line contains only digits (Arabic numerals)
    return bool(re.match(r"^\d+$", last_line)) and int(last_line) == expected_page_number


def is_sequential(page_numbers):
    # Ensure page numbers are sequential
    return page_numbers == list(range(1, len(page_numbers) + 1))
