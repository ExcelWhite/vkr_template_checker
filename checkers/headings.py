from extractors.headings import extract_headings_from_document


def check_headings(doc):
    # Initialize the flags
    is_in_order = True
    required_heading_missing = False

    headings = extract_headings_from_document(doc)

    # Define the required headings in the expected order
    required_headings = [
        "ВВЕДЕНИЕ",
        "ЗАКЛЮЧЕНИЕ",
        "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ",
        "ПРИЛОЖЕНИЕ A"
    ]

    # Step 1: Check if all required headings are present
    for heading in required_headings:
        if heading not in headings:
            required_heading_missing = True
            print(f"❌ Missing heading: {heading}")

    # Step 2: Check if headings are in the correct order
    for i in range(len(required_headings) - 1):
        if headings.index(required_headings[i]) > headings.index(required_headings[i + 1]):
            is_in_order = False
            print(f"❌ Incorrect order: '{required_headings[i]}' should come before '{required_headings[i + 1]}'")

    # Step 3: Return result based on checks
    if required_heading_missing:
        return {"Headings Check": "❌ One or more required headings are missing."}
    elif not is_in_order:
        return {"Headings Check": "❌ Headings are not in the correct order."}

    return {"Headings Check": "✅ Pass: All required headings are present and in the correct order."}
