import ollama
from src.config import VISION_MODEL

PROMPT="""This image is a chart. Its caption is: "{caption}"

Describe the chart in 2-3 sentences:
- Start with the chart type, using exactly one of these: "line chart", "stacked bar chart", "grouped bar chart", "pie chart", "diagram", "map".
  Stacked bars = parts on top of each other in one bar; grouped bars = separate bars side by side.
- Say what each line, bar or colour represents (translate legend names to English):
  left to right for grouped bars, top to bottom for lines and stacked bars.
- For line charts, say which line is higher and which is lower on the chart.
- Give the units. If no units are shown (for example in a diagram), do not write anything about units.
- Translate Romanian abbreviations: GES = GHG (greenhouse gases), SRE = RES (renewable energy sources).

Do not list any numbers from the chart."""

def describe_chart(image_path, caption):
    response=ollama.chat(
        model=VISION_MODEL,
        messages=[{
            "role":"user",
            "content":PROMPT.format(caption=caption),
            "images":[image_path],
        }], options={"temperature":0, "num_ctx": 8192},
    )
    return response["message"]["content"]

if __name__ == "__main__":
    from src.config import DATA_DIR
    from src.charts.extract_charts import find_charts, save_chart_images
    from src.config import OUTPUT_DIR

    pdf_path=DATA_DIR / "romania" / "First_NECP_Romania.pdf"
    charts=find_charts(pdf_path)
    charts=save_chart_images(pdf_path, charts, OUTPUT_DIR / "charts" / "images")

    for chart in charts:
        if chart["chart_id"] in ["p48_c0", "p62_c0", "p57_c0"]:
            print(f"\n=== p{chart['page']} | {chart['caption']}")
            print(describe_chart(chart["image"], chart["caption"]))