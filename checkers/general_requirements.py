from collections import Counter

from extractors.fonts import extract_font_info
from extractors.margins import extract_margins
from extractors.page_info import extract_page_sizes
from helper_functions.helper_functions import estimate_line_spacing


def check_page_size_requirement(page_sizes, expected_size=(210, 297), tolerance=2.0):
    expected_width, expected_height = expected_size
    return all(
        abs(w - expected_width) <= tolerance and abs(h - expected_height) <= tolerance
        for w, h in page_sizes
    )


def check_font_size_requirement(font_sizes, min_size=12):
    return all(size >= min_size for size in font_sizes)


# def check_font_type_requirement(font_names, expected_font="TimesNewRoman"):
#     return all(expected_font in font for font in font_names)

def check_font_type_requirement(font_names, expected_font="TimesNewRoman"):
    non_expected_fonts = {font for font in font_names if expected_font not in font}
    return len(non_expected_fonts) == 0, non_expected_fonts


def check_font_color_requirement(font_colors, expected_color="#000000"):
    return all(color.lower() == expected_color for color in font_colors)


# LINE SPACING (approximate)
def check_line_spacing_requirement(doc, expected_spacing=20, tolerance=2):
    all_spacings = []
    for page in doc:
        all_spacings.extend(estimate_line_spacing(page))
    if not all_spacings:
        return False
    common_spacing = Counter(round(sp) for sp in all_spacings).most_common(1)[0][0]
    return abs(common_spacing - expected_spacing) <= tolerance


def check_margin_requirement(margins, expected_margins=(30, 15, 20, 20)):
    """Check if all margins match the expected margins (left 30mm, right 15mm, top 20mm, bottom 20mm)."""
    return all(
        (left == expected_margins[0] and
         right == expected_margins[1] and
         top == expected_margins[2] and
         bottom == expected_margins[3])
        for left, right, top, bottom in margins
    )


# MAIN CHECK FUNCTION
def check_general_requirements(doc):
    results = {}

    # Page size check
    page_sizes = extract_page_sizes(doc)
    if check_page_size_requirement(page_sizes):
        results["Page Size"] = "✅ Pass: All pages are A4"
    else:
        results["Page Size"] = f"❌ Fail: Non-A4 pages detected, sizes: {page_sizes}"

    # Font info checks
    font_sizes, font_names, font_colors = extract_font_info(doc)
    if check_font_size_requirement(font_sizes):
        results["Font Size"] = "✅ Pass: All font sizes are 12pt or more"
    else:
        results["Font Size"] = "❌ Fail: Font sizes below 12pt found"

    is_pass, non_expected_fonts = check_font_type_requirement(font_names)
    if is_pass:
        results["Font Type"] = "✅ Pass: All fonts are Times-Roman"
    else:
        results["Font Type"] = f"❌ Fail: Non-Times-Roman fonts found: {non_expected_fonts}"

    if check_font_color_requirement(font_colors):
        results["Font Color"] = "✅ Pass: All fonts are black"
    else:
        results["Font Color"] = f"❌ Fail: Non-black font colors detected: {set(font_colors)}"

    # Line spacing
    if check_line_spacing_requirement(doc):
        results["Line Spacing"] = "✅ Pass: Line spacing is approximately correct"
    else:
        results["Line Spacing"] = "❌ Fail: Line spacing deviates from expected"

    # Check margins
    margins = extract_margins(doc)
    if check_margin_requirement(margins):
        results["Margins"] = "✅ Pass: Margins are as expected (left 30mm, right 15mm, top 20mm, bottom 20mm)"
    else:
        found_margins = ', '.join(
            f"Page {i + 1}: Left: {margins[i][0]}, Right: {margins[i][1]}, Top: {margins[i][2]}, "
            f"Bottom: {margins[i][3]}" for i in range(len(margins)))
        results["Margins"] = f"❌ Fail: Margins are not as expected. Found margins: {found_margins}"

    return results
