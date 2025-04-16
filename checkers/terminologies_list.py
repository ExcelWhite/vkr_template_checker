import re

from extractors.headings import extract_heading_by_name


def check_terminologies_list(doc):
    result = {}
    target_heading = "Список сокращений и условных обозначений"

    page_num, matched_heading = extract_heading_by_name(doc, target_heading.upper())

    if page_num is None:
        return {"Abbreviations Check": f"⚠️ Heading '{target_heading}' not found in document."}

    # Extract lines from the page (PDF pages are 0-indexed)
    page = doc[page_num - 1]
    lines = page.get_text("text").splitlines()

    # Locate heading in the actual text
    heading_idx = None
    for i, line in enumerate(lines):
        if matched_heading.lower().strip() in line.lower().strip():
            heading_idx = i
            break

    if heading_idx is None:
        return {"Abbreviations Check": f"⚠️ Heading '{matched_heading}' found in metadata but not in page text."}

    # Extract all lines after the heading
    content_lines = lines[heading_idx + 1:]

    # Clean: remove empty lines or lines with only whitespace
    content_lines = [line.strip() for line in content_lines if line.strip()]

    # Remove page number line if present (e.g., "12")
    if content_lines and re.fullmatch(r"\d{1,3}", content_lines[-1]):
        content_lines.pop()

    # Now skip the first line after cleaning (e.g., if heading is repeated in layout)
    content_lines = content_lines[1:]

    if len(content_lines) == 1 and content_lines[0].lower() == "текст":
        return {"Abbreviations Check": "⚠️ Only the word 'текст' found instead of abbreviation examples."}

    # Validate lines using pattern: {abbr} - {description}
    invalid_lines = []
    pattern = r"^[^\s\-]{1,10}\s*-\s+.+"

    for line in content_lines:
        if not re.match(pattern, line):
            invalid_lines.append(line)

    if invalid_lines:
        result["Invalid Entries"] = "❌ Invalid abbreviation lines:\n" + "\n".join(f"   - {l}" for l in invalid_lines)
    else:
        result["Abbreviations Check"] = "✅ Pass: All abbreviations are correctly formatted."

    return result
