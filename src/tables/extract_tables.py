import pymupdf
from src.config import DOC_SETTINGS, DEFAULT_SETTINGS


def extract_caption(page, table, running_header):
    x0,y0,x1,y1=table.bbox
    caption_area=pymupdf.Rect(0, max(0,y0-60), page.rect.width, y0)
    caption=page.get_text("text", clip=caption_area).strip()
    lines=caption.split("\n")
    for i in reversed(range(len(lines))):
        if lines[i].strip().startswith("Table"):
            return  " ".join(" ".join(lines[i:]).split())

    caption=" ".join(caption.split())
    if running_header and running_header in caption:
        return ""
    return caption

white=(1.0, 1.0, 1.0)
def has_visible_lines(page, table):
    rectangles=page.get_drawings()
    for drawing in rectangles:
        if not drawing["rect"].intersects(table.bbox):
            continue

        colour=drawing.get("color") or drawing.get("fill")
        if colour is not None and tuple(colour)!=white:
            return True

    return False


def extract_tables(pdf_path):
    settings=DOC_SETTINGS.get(pdf_path.name, DEFAULT_SETTINGS)
    doc=pymupdf.open(pdf_path)
    tables=[]

    for page_num, page in enumerate(doc, start=1):
        found_tables=page.find_tables(strategy="lines")

        for table_num, table in enumerate(found_tables.tables):
            if settings["skip_2_col"] and table.col_count<3:
                continue

            if not has_visible_lines(page, table):
                continue

            caption=extract_caption(page, table, settings["running_header"])
            if caption.startswith(("Chart", "Figure", "Graph")):
                continue

            rows=table.extract()
            if not table.header.external and len(rows)>1:
                rows=rows[1:]

            tables.append({
                "source": pdf_path.name,
                "page": page_num,
                "table_id": f"p{page_num}_t{table_num}",
                "caption": caption,
                "headers": table.header.names,
                "data": rows
            })

    doc.close()
    return tables






