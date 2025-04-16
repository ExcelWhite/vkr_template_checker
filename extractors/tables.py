from typing import List, Dict


def extract_tables_from_document(doc) -> List[Dict]:
    """
    Extract tables from the document.
    Assumes each table will have a 'caption' field, containing the name or description.
    Returns a list of dictionaries where each dictionary represents a table.
    """
    tables = []

    # Loop through pages and extract tables
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        table = None

        for block in blocks:
            if "lines" not in block:
                continue

            for line in block["lines"]:
                if not line["spans"]:
                    continue
                text = ''.join([span["text"] for span in line["spans"]]).strip()

                # Identify tables by certain patterns (e.g., "Таблица")
                if text.startswith("Таблица"):
                    # Check if it starts with "Таблица"
                    table = {'caption': text, 'columns': []}
                    tables.append(table)

                # Optionally, extract table columns (e.g., from lines in the same block)
                if table and text:
                    table['columns'].append(text)  # Collect table column data

    return tables
