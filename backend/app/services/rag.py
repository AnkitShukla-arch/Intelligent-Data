"""RAG + NLQ service. Answers queries using vector retrieval + OpenAI LLM."""
import os
from typing import Dict, Any
from app.core.config import settings
from app.services import vector_store as vs

FRESHER_SYSTEM = (
    "You are a friendly senior colleague helping a new intern. "
    "Always explain technical terms in simple words. Be warm and encouraging. "
    "Never make the person feel bad for asking basic questions."
)

EXPERT_SYSTEM = (
    "You are a precise corporate AI assistant. "
    "Answer concisely and factually, citing the provided context."
)


def _build_prompt(system: str, context: str, query: str) -> str:
    return (
        f"System: {system}\n\n"
        f"Context extracted from company documents:\n---\n{context}\n---\n\n"
        f"Question: {query}\n\nAnswer:"
    )


def answer_query(query: str, fresher_mode: bool = False) -> Dict[str, Any]:
    """Main entry: retrieve relevant chunks, then call LLM."""
    # 1. SQL-heuristic queries (MVP)
    lower = query.lower()
    if any(k in lower for k in ["how many", "count", "total hours", "who logged", "last log"]):
        return {
            "answer": (
                "📊 This looks like an analytics query. "
                "The analytics dashboard (top menu → Analytics) can answer this—"
                "it shows real-time stats from the work-log database."
            ),
            "sources": []
        }

    # 2. Vector retrieval
    docs = vs.similarity_search(query, k=4)
    if not docs:
        no_context_msg = (
            "I don't have enough documents in the knowledge base yet to answer this. "
            "Please upload relevant documents first via the Upload page."
        )
        return {"answer": no_context_msg, "sources": []}

    context = "\n\n".join(d.page_content for d in docs)
    sources = list({d.metadata.get("source", "Unknown") for d in docs})

    # 3. LLM call
    if not settings.OPENAI_API_KEY:
        return {
            "answer": (
                "⚠️ OpenAI API key not configured. Add OPENAI_API_KEY to your .env file. "
                f"Context found from: {', '.join(sources)}"
            ),
            "sources": sources,
        }

    try:
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        system = FRESHER_SYSTEM if fresher_mode else EXPERT_SYSTEM
        prompt = _build_prompt(system, context, query)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"},
            ],
            max_tokens=600,
            temperature=0.3,
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        answer = f"LLM error: {e}"

    return {"answer": answer, "sources": sources}
