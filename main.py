import fitz
import sys

from checkers.general_requirements import check_general_requirements
from checkers.illustrations import check_illustrations
from checkers.page_numeration import check_page_numeration
from checkers.reference_list import check_reference_list
from checkers.simple_text_sections_check import check_simple_text_sections
from checkers.table_of_contents import check_table_of_contents
from checkers.headings import check_headings
from checkers.tables import check_tables
from checkers.terminologies_list import check_terminologies_list


def load_document(path):
    try:
        doc = fitz.open(path)
        return doc
    except FileNotFoundError:
        print(f"❌ Error: The file '{path}' was not found.")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def check_basic_structure(doc):
    return bool(doc and len(doc) > 0)


def generate_report(results):
    """Generate a structured report from the results with tabulation and gaps between lines."""
    report = []

    # Loop through categories in results (e.g., 'general', 'content')
    for category, category_results in results.items():
        report.append(f"*****{category.upper()}*****\n")  # Category header

        # Loop through each result in the category (check results like 'Page Size', 'Font Size', etc.)
        for check, result in category_results.items():
            report.append(f"\t--- {check} ---\n")  # Tabulate each check
            if isinstance(result, str):  # If result is a simple string (pass/fail message)
                report.append(f"\t{result}\n")  # Indent and add a line gap
            elif isinstance(result, list):  # If result is a list (like missing headings, errors)
                for item in result:
                    report.append(f"\t- {item}\n")  # Indent and add a line gap
            else:
                report.append(f"\t{str(result)}\n")  # Handle any other case, just in case

        # Add a line gap between categories
        report.append("\n")

    return "".join(report)


if __name__ == "__main__":
    file_path = "doc.pdf"

    # LOAD DOCUMENT
    document = load_document(file_path)
    if document is None:
        print("❌ Error: Unable to read document")
        sys.exit(1)
    else:
        print("✅ Document loaded successfully")

    # CHECK BASIC STRUCTURE
    isProcessable = check_basic_structure(document)
    if isProcessable:
        print("✅ Document is processable")
    else:
        print("❌ Document is not processable")
        sys.exit(2)

    # Initialize results map
    results = {
        "general": check_general_requirements(document),
        "content": check_table_of_contents(document),
        "headings": check_headings(document),
        "page numeration": check_page_numeration(document),
        "illustrations": check_illustrations(document),
        "tables": check_tables(document),
        "list of terminologies": check_terminologies_list(document),
        "reference list": check_reference_list(document),
        "simple text checks": check_simple_text_sections(document)
    }

    # Run checks

    # Generate report
    report = generate_report(results)
    print(report)
