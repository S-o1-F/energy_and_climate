import ollama
from src.config import LLM_MODEL
from src.search import search
import sys

PROMPT = """Answer the question using ONLY the context below.
Cite the page for every fact, like (page 50).

Context:
{context}

Question: {question}

Start your answer with "According to page N," where N is the page the answer comes from.
Answer:"""

def build_context(results):
    return "\n\n".join(f"[{source}, page {page}]\n{content}"
                       for source, page, section, content, sim in results)


def answer(question: str, country: str = "RO", k: int = 5):
    results = search(question, country=country, k=k)
    prompt = PROMPT.format(context=build_context(results), question=question)
    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0, "num_ctx": 4096},
    )
    return response["message"]["content"], results




if __name__ == "__main__":
    """question = ("Current and projected progress towards other national greenhouse-gas related "
                "targets and objectives, including sector targets")
    question = ("National contribution and indicative trajectory for primary and final energy consumption - "
                "Translation into absolute level of primary energy consumption (PEC)")"""
    question=sys.argv[1]
    text, results=answer(question)
    print(f"Q: {question}")
    print(f"Retrieved pages: {[r[1] for r in results]}")
    print(f"A: {text}")
