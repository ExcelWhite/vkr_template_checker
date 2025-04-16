import fitz
import re
from typing import List, Tuple


def extract_toc_from_first_page(doc) -> List[Tuple[str, int]]:
    toc_entries: List[Tuple[str, int]] = []
    first_page = doc[0]

    # Filter non-empty and non-space-only lines
    lines = [line.strip() for line in first_page.get_text("text").split('\n') if line.strip()]

    # Ensure last line isn't just a page number (e.g., page numeration footer)
    if lines and re.fullmatch(r'\d+', lines[-1]):
        lines = lines[:-1]

    # Ensure the first non-empty line is "СОДЕРЖАНИЕ"
    if not lines or lines[0].upper() != "СОДЕРЖАНИЕ":
        print("❌ TOC must start with 'СОДЕРЖАНИЕ'")
        return []

    # Process lines following "СОДЕРЖАНИЕ"
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue

        # Match lines with either dots or multiple spaces before the page number
        # e.g., "1.1. Heading......3", "Heading     4", etc.
        title_match = re.match(r'(.+?)(?:\.{2,}|\s{3,})', line)
        page_match = re.search(r'(\d+)$', line)

        if title_match and page_match:
            title = title_match.group(1).strip()
            page = int(page_match.group(1))
            toc_entries.append((title, page))

    return toc_entries
