import re


def estimate_line_spacing(page):
    spacings = []
    previous_y = None
    valid_lines_y = []  # To store the Y coordinates of non-empty lines

    blocks = page.get_text("dict")["blocks"]
    for block in blocks:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            # Extract the text from the line
            line_text = ''.join(span['text'] for span in line['spans'])

            # Check if the line is not empty and does not contain only whitespace
            if line_text.strip():  # Only consider non-empty lines
                y = line["bbox"][1]  # Top Y coordinate
                valid_lines_y.append(y)  # Store the Y coordinate of valid lines

    # Exclude the last line (assumed to be the page number)
    if len(valid_lines_y) > 1:
        for i in range(len(valid_lines_y) - 2):
            spacing = abs(valid_lines_y[i + 1] - valid_lines_y[i])
            spacings.append(spacing)
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
