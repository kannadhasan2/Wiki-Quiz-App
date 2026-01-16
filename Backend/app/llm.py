import json
import re
from typing import Any, Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from app.config import GEMINI_API_KEY

llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    google_api_key=GEMINI_API_KEY,
    temperature=0.2,
)

PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are a precise education content generator. "
     "You MUST only use facts present in the article text. "
     "Return STRICT JSON only. No markdown. No extra text."),
    ("user",
     """Wikipedia Article Title: {title}

Article Summary:
{summary}

Article Sections:
{sections}

Article Text (may be long, clipped):
{text}

TASK:
Return a single JSON object with EXACT keys:
- key_entities: {{ "people": [...], "organizations": [...], "locations": [...] }}
- quiz: array of 5 to 10 objects, each:
  {{
    "question": "...",
    "options": ["A", "B", "C", "D"],
    "answer": "exactly one of the options",
    "difficulty": "easy" | "medium" | "hard",
    "explanation": "1-2 sentences grounded in the article"
  }}
- related_topics: 5 to 10 strings (Wikipedia topic names)

CONSTRAINTS:
- No hallucinations: if unsure, avoid that fact.
- Options must be plausible and grounded in the article context.
- answer must match one option exactly.
- Keep explanations short and specific.

Return STRICT JSON only."""
    )
])

def _extract_json(text: str) -> str:
    """
    Gemini sometimes returns extra whitespace or fenced blocks.
    We extract the first top-level JSON object.
    """
    text = text.strip()
    # remove code fences if present
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    # find first {...} block (best-effort)
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("LLM did not return a JSON object.")
    return text[start:end+1]

def generate_quiz_payload(title: str, summary: str | None, sections: list[str], full_text: str) -> Dict[str, Any]:
    # clip to reduce token load, but keep useful density
    clipped = full_text[:12000]

    msg = PROMPT.format_messages(
        title=title,
        summary=summary or "",
        sections=", ".join(sections[:20]),
        text=clipped
    )

    resp = llm.invoke(msg)
    raw = resp.content if hasattr(resp, "content") else str(resp)

    json_str = _extract_json(raw)
    data = json.loads(json_str)

    # minimal sanity checks
    if "quiz" not in data or "related_topics" not in data or "key_entities" not in data:
        raise ValueError("LLM JSON missing required keys (quiz/related_topics/key_entities).")

    return data
