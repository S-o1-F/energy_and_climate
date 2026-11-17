import ollama
from src.config import LLM_MODEL
from src.search import search
import sys
import re

PROMPT = """Answer the question using ONLY the context below.
Cite the document and page for every fact, like (RS_NECP.pdf, page 50).

Context:
{context}

Question: {question}

Start your answer with "According to <document>, page N," using the document name and page shown above the context you used.
Answer:"""

def build_context(results):
    return "\n\n".join(f"[{source}, page {page}]\n{content}"
                       for source, page, section, content, sim in results)


def answer(question: str, country: str = "RS", k: int = 5):
    results = search(question, country=country, k=k)
    prompt = PROMPT.format(context=build_context(results), question=question)
    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0, "num_ctx": 4096},
    )
    return response["message"]["content"], results

def find_source(answer_text, results):
    parts=answer_text.split(",", 2)
    if len(parts)==3:
        answer_text = parts[2]
    numbers=re.findall(r"\d[\d.,]*\d", answer_text)
    best_chunk=None
    best_count=0
    for chunk in results:
        source, page, section, content, similarity=chunk
        count=0
        for number in numbers:
            if number in content:
                count+=1
            if count>best_count:
                best_chunk=(source, page)
                best_count=count
    return best_chunk


if __name__ == "__main__":
    """question = ("Current and projected progress towards other national greenhouse-gas related "
                "targets and objectives, including sector targets")
    question = ("National contribution and indicative trajectory for primary and final energy consumption - "
                "Translation into absolute level of primary energy consumption (PEC)")"""
    question=sys.argv[1]
    text, results=answer(question)
    source = find_source(text, results)
    if source:
        text = re.sub(r"^According to .*?, page \d+,", f"According to {source[0]}, page {source[1]},", text)
    print(f"Q: {question}")
    print(f"Retrieved pages: {[r[1] for r in results]}")
    print(f"A: {text}")
