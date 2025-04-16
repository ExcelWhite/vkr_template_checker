def extract_font_info(doc):
    font_sizes = []
    font_names = []
    font_colors = []

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    font_sizes.append(span["size"])
                    font_names.append(span["font"])
                    color = span.get("color", 0)
                    font_colors.append("#{0:06x}".format(color))
    return font_sizes, font_names, font_colors
