import fitz  # PyMuPDF

def extract_sections_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)

    # Step 1: Collect all font sizes
    font_sizes = set()
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    font_sizes.add(span["size"])

    # Step 2: Define top 3 heading levels
    top_sizes = sorted(font_sizes, reverse=True)[:3]
    size_to_level = {sz: f"H{idx+1}" for idx, sz in enumerate(top_sizes)}

    sections = []
    current = None

    for page_number, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                line_text = ""
                if not line["spans"]:
                    continue
                size = line["spans"][0]["size"]
                for span in line["spans"]:
                    line_text += span["text"].strip() + " "
                line_text = line_text.strip()

                if size in size_to_level:
                    # Start a new section
                    current = {
                        "document": pdf_path.split("/")[-1],
                        "page_number": page_number,
                        "section_title": line_text,
                        "level": size_to_level[size],
                        "content": ""
                    }
                    sections.append(current)
                elif current:
                    current["content"] += " " + line_text

    return sections
