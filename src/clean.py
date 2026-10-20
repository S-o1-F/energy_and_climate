import json
import re
from pathlib import Path

def clean_text(text: str) -> str:

    # only keep \n
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # za tab
    text = re.sub(r"[ \t]+", " ", text)

    # "report-\ning" -> "reporting"
    text = re.sub(
        r"(?<=[A-Za-z])-\n(?=[a-z])",
        "",
        text
    )

    # celosna recenica
    text = re.sub(
        r"(?<!\n)\n(?!\n)",
        " ",
        text
    )

    # replace 3 or more newlines with 1 newline
    text = re.sub(r"\n{3,}", "\n\n", text)

    # remove page number at the end
    #text=re.sub(r"\n+\s*\d+\s*$", "", text)

    return text.strip()


def is_table_of_contents(text: str) -> bool:

    first_lines = text.strip().splitlines()[:5]

    return any(
        line.strip().upper() in {
            "CONTENTS",
            "TABLE OF CONTENTS"
        }
        for line in first_lines
    )


def clean_document(input_path, output_path):

    with open(input_path, "r", encoding="utf-8") as file:
        pages = json.load(file)

    cleaned_pages = []

    for page in pages:

        original_text = page["text"]

        if is_table_of_contents(original_text):
            continue

        cleaned_text = clean_text(original_text)

        if not cleaned_text:
            continue

        cleaned_pages.append({
            **page,
            "text": cleaned_text
        })

    output_path = Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:

        json.dump(cleaned_pages, file, ensure_ascii=False, indent=2)

    print(f"Cleaned {len(cleaned_pages)} pages.")


if __name__ == "__main__":

    clean_document(
        "../data/extracted/Dataflow1-GHG.json",
        "../data/cleaned/Dataflow1-GHG.json"
    )
