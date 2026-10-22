import re
import json
from src.config import OUTPUT_DIR



def normalize_whitespace(text: str) -> str:

    # za tab
    text = re.sub(r"[ \t]+", " ", text)

    lines=text.splitlines()
    cleaned_lines=[]
    for line in lines:
        cleaned_line=line.strip()
        cleaned_lines.append(cleaned_line)

    text="\n".join(cleaned_lines)

    # replace 3 or more newlines with 2 newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()

def remove_repeated_header(text:str)->str:
    header="The 2021-2030 Integrated National Energy and Climate Plan"
    text=text.replace(header, "")
    return text


def clean_text(text: str) -> str:
    text=remove_repeated_header(text)
    text = normalize_whitespace(text)
    return text

def clean_pages(pages: list)->list:
    cleaned_pages=[]
    for page in pages:
        cleaned_pages.append({
            **page,
            "text": clean_text(page["text"])
        })

    return cleaned_pages


if __name__ == "__main__":

    input_path = OUTPUT_DIR / "extracted" / "First_NECP_Romania.json"

    output_path = OUTPUT_DIR / "cleaned" / "First_NECP_Romania.json"

    with open(input_path, "r", encoding="utf-8") as file:
        pages = json.load(file)

    cleaned_pages = clean_pages(pages)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(cleaned_pages, file, ensure_ascii=False, indent=2)

    print(f"Cleaned {len(cleaned_pages)} pages.")

