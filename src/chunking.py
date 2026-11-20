import re

HEADING=re.compile(r"^[1-9](\.\d{1,2})+\.?\s+[A-Z][a-z]{2,}")
UNITS=("Mtoe", "ktoe", "Mt", "TWh", "GWh", "Million", "Billion")
CHAPTER_CONTEXT={
    "4": "Current situation and projections with existing measures (WEM scenario)",
    "5": "Impact of planned policies and measures (WAM scenario / scenario S)",
}

def find_heading(line):
    line=" ".join(line.split())
    if HEADING.match(line) and "...." not in line:
        if not line.split(" ",1)[1].startswith(UNITS):
            return line
    return None

def chunk_pages(pages: list[dict], country: str,chunk_size: int=200, overlap:int=40, )->list[dict]:
    chunks=[]
    step=chunk_size-overlap
    heading=""

    for page in pages:
        words=[]
        word_headings=[]
        for line in page["text"].split("\n"):
            found=find_heading(line)
            if found:
                heading=found
            for word in line.split():
                words.append(word)
                word_headings.append(heading)

        for j, start in enumerate(range(0, len(words), step)):
            piece=" ".join(words[start:start+chunk_size])
            if not piece:
                continue
            section=word_headings[start]
            chapter=CHAPTER_CONTEXT.get(section[:1], "")
            context=" ".join(part+"." for part in [chapter, section] if part)+" "
            chunks.append({
                "id": f"{page['source']}_p{page['page']}_c{j}",
                "source": page['source'],
                "country": country,
                "page": page['page'],
                "text": context+piece,
            })

    return chunks
