import json
from ocrmac import ocrmac
from src.charts.extract_charts import find_charts, save_chart_images
from src.charts.describe_charts import describe_chart
from src.charts.chart_values import values_per_label
from src.tables.chunk_tables import COUNTRY_NAMES

#ocr values, qwen desciption

def chart_to_chunk(chart, description, values, country):

    name=COUNTRY_NAMES.get(country, country)
    text=f"{name}. {chart['caption']}.\n{description}"
    if values:
        text+=f"\nValues printed on the chart, by year:\n{values}"
    return {
        "id": f"{chart['source']}_{chart['chart_id']}",
        "country": country,
        "source": chart["source"],
        "page": chart["page"],
        "section": chart["caption"],
        "text": text,
        "values": values,
        "image": chart["image"],
    }

def charts_to_chunks(pdf_path, country, image_dir):
    chunks=[]
    charts=find_charts(pdf_path)
    charts = [c for c in charts if c["chart_id"] in [
        "p48_c0", "p51_c0", "p52_c0", "p53_c0", "p54_c0", "p57_c0", "p59_c0", "p59_c1",
        "p62_c0", "p154_c0", "p209_c0", "p209_c1"]]
    charts=save_chart_images(pdf_path, charts, image_dir)
    for chart in charts:
        ocr_result=ocrmac.OCR(chart["image"], recognition_level="accurate").recognize()
        description=describe_chart(chart["image"], chart["caption"])
        values = values_per_label(ocr_result)
        chunks.append(
            chart_to_chunk(chart, description, values, country)
        )
        print(f"done p{chart['page']} {chart['chart_id']}")
    return chunks


if __name__ == "__main__":
    from src.config import DATA_DIR, OUTPUT_DIR

    pdf_path=DATA_DIR / "romania" / "First_NECP_Romania.pdf"
    chunks=charts_to_chunks(pdf_path, "RO", OUTPUT_DIR / "charts" / "images")

    # Save the chunks, so the slow part (Qwen) only runs once.
    path=OUTPUT_DIR / "charts" / f"{pdf_path.stem}_chart_chunks.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)
    print(f"{len(chunks)} chart chunks saved to {path}")