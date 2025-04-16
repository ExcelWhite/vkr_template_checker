from extractors.headings import extract_heading_by_name


def check_simple_text_sections(doc):
    result = {}
    headings_to_check = ["ПРИЛОЖЕНИЕ A", "ВВЕДЕНИЕ", "ЗАКЛЮЧЕНИЕ"]

    for target_heading in headings_to_check:
        page_num, matched_heading = extract_heading_by_name(doc, target_heading.upper())
        if page_num is None:
            result[target_heading] = f"⚠️ Heading '{target_heading}' not found in document."
            continue

        # Get the page text as lines
        page = doc[page_num - 1]
        lines = page.get_text("text").splitlines()

        # Find the heading index
        heading_idx = None
        for i, line in enumerate(lines):
            if matched_heading.lower().strip() in line.lower().strip():
                heading_idx = i
                break

        if heading_idx is None or heading_idx + 1 >= len(lines):
            result[target_heading] = f"❌ Could not find a line after the heading '{target_heading}'."
            continue

        next_line = lines[heading_idx + 1].strip().lower()
        if next_line == "текст":
            result[target_heading] = f"✅ Pass: '{target_heading}' section content starts with 'текст'"
        else:
            result[target_heading] = f"❌ Expected 'текст' after '{target_heading}', but found: '{lines[heading_idx + 1].strip()}'"

    return result
