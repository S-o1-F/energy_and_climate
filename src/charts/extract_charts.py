import re
import pymupdf

CAPTION=re.compile(r"^(Chart|Figure|Graph)\s*[\d.]+\s*[:–-]")

def get_caption(block_text):
    lines=block_text.replace("Error! No text of specified style in document.","").split("\n")
    for i in range(len(lines)):
        if CAPTION.match(lines[i].strip()):
            caption=" ".join(lines[i:]).strip()
            if "...." not in caption:
                return caption
    return None

def get_chart_bottom(blocks, top, page_height):
    for block in blocks:
        text=" ".join(block[4].split())
        if block[1] > top + 20:
            if len(text) > 60 or text.startswith(("Source", "Chart", "Figure", "Graph", "Table")):
                return block[1] + 10
    return page_height - 40

def find_charts(pdf_path):
    doc=pymupdf.open(pdf_path)
    charts=[]
    for page_num, page in enumerate(doc, start=1):
        blocks=sorted(page.get_text("blocks"), key=lambda b: b[1])
        chart_num=0
        for block in blocks:
            caption=get_caption(block[4])
            if caption is None:
                continue

            top=block[3]
            bottom=get_chart_bottom(blocks, top, page.rect.height)
            if bottom-top<80:
                continue
            charts.append({
                "source": pdf_path.name,
                "page": page_num,
                "chart_id": f"p{page_num}_c{chart_num}",
                "caption": caption,
                "bbox": [0, top, page.rect.width, bottom],
            })
            chart_num+=1
    doc.close()
    return charts

def save_chart_images(pdf_path, charts,output_dir):
    doc=pymupdf.open(pdf_path)
    for chart in charts:
        page=doc[chart["page"]-1]
        image=page.get_pixmap(dpi=300, clip=pymupdf.Rect(chart["bbox"]))
        path=output_dir / f"{pdf_path.stem}_{chart['chart_id']}.png"
        image.save(path)
        chart["image"]=str(path)
    doc.close()
    return charts


if __name__ == "__main__":
    from src.config import DATA_DIR, OUTPUT_DIR

    pdf_path=DATA_DIR / "romania" / "First_NECP_Romania.pdf"
    charts=find_charts(pdf_path)
    charts=[c for c in charts if c["chart_id"] in ["p48_c0", "p57_c0", "p62_c0"]]
    save_chart_images(pdf_path, charts, OUTPUT_DIR / "charts" / "images")

    print(f"{len(charts)} charts saved")
    for c in charts[:10]:
        print(f"p{c['page']} | {c['caption'][:70]}")