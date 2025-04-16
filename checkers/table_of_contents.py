from extractors.headings import extract_headings_from_document, extract_headings_from_document_with_page_number
from extractors.table_of_contents import extract_toc_from_first_page
from helper_functions.helper_functions import compare_toc_and_headings


def check_table_of_contents(doc):
    toc = extract_toc_from_first_page(doc)
    headings = extract_headings_from_document_with_page_number(doc)


    missing, extra = compare_toc_and_headings(toc, headings)

    result = {}
    if not toc:
        result["TOC Check"] = "❌ No TOC found"
    elif not missing and not extra:
        result["TOC Check"] = "✅ Pass: TOC matches actual headings"
    else:
        result["TOC Check"] = "⚠️ Partial match"
        if missing:
            result["Missing from Document"] = missing
        if extra:
            result["Extra in Document"] = extra

    return result