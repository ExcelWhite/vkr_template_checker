import re

from extractors.headings import extract_heading_by_name
from helper_functions.helper_functions import clean_text


def check_reference_list(doc):
    result = {}
    target_heading = "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ"

    page_num, matched_heading = extract_heading_by_name(doc, target_heading.upper())

    if page_num is None:
        return {"Reference List Check": f"⚠️ Heading '{target_heading}' not found in document."}

    page = doc[page_num - 1]
    raw_lines = page.get_text("text").splitlines()

    # Clean lines and filter out empty ones and page number line
    lines = [
        clean_text(line) for line in raw_lines
        if clean_text(line) and not re.match(r"^\d{1,3}$", clean_text(line))
    ]

    # Find heading index again (cleaned)
    heading_idx = None
    for i, line in enumerate(lines):
        if matched_heading.lower().strip() in line.lower().strip():
            heading_idx = i
            break

    if heading_idx is None:
        return {"Reference List Check": f"⚠️ Heading '{matched_heading}' found in metadata but not in page text."}

    content_lines = lines[heading_idx + 1:]

    # Merge lines where number and source text were separated
    merged_lines = []
    i = 0
    while i < len(content_lines):
        current_line = content_lines[i]
        if re.match(r"^\d+\.$", current_line):
            # e.g. "1." followed by "Источник 1"
            if i + 1 < len(content_lines):
                merged_line = f"{current_line} {content_lines[i + 1]}"
                merged_lines.append(merged_line)
                i += 2
            else:
                merged_lines.append(current_line)
                i += 1
        else:
            merged_lines.append(current_line)
            i += 1

    # Validate format "1. source text"
    invalid_lines = [line for line in merged_lines if not re.match(r"^\d+\.\s+.+", line)]

    if not merged_lines:
        return {"Reference List Check": "⚠️ No reference entries found after the heading."}
    elif invalid_lines:
        result["Invalid Entries"] = "❌ Some entries are not correctly numbered:\n" + "\n".join(f"   - {l}" for l in invalid_lines)
    else:
        result["Reference List Check"] = "✅ Pass: All references are numbered correctly."

    return result
