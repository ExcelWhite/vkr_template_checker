def extract_illustrations_from_document(doc):
    # Assuming the document contains illustrations and captions as separate elements
    illustrations = []

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                if not line["spans"]:
                    continue
                text = ''.join([span["text"] for span in line["spans"]]).strip()

                # Look for captions that start with "Рисунок"
                if text.startswith("Рисунок"):
                    illustrations.append({'caption': text})

    return illustrations