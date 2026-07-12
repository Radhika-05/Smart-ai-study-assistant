"""
Gemini Service — enhanced study intelligence layer.

Returns richer output: summary, keywords, questions, topic, difficulty,
key_concepts, and mnemonics.
"""

import json
import os
import re
from typing import Optional

import google.generativeai as genai

EXPECTED_KEYS = {"summary", "keywords", "questions"}

SUMMARY_INSTRUCTIONS = {
    "Short":    "Write a concise summary in 2–3 sentences.",
    "Medium":   "Write a clear summary in 4–6 sentences covering the main ideas.",
    "Detailed": "Write a comprehensive summary in 8–12 sentences covering all key concepts and details.",
}


def _build_prompt(text: str, summary_length: str, num_questions: int) -> str:
    summary_instruction = SUMMARY_INSTRUCTIONS.get(summary_length, SUMMARY_INSTRUCTIONS["Medium"])
    return f"""You are an expert study assistant and educator. Analyze the following notes and return ONLY a valid JSON object — no markdown fences, no preamble, nothing outside the JSON.

Schema:
{{
  "summary": "string",
  "keywords": ["string"],
  "questions": ["string"],
  "topic": "string",
  "difficulty": "Easy" | "Medium" | "Hard",
  "key_concepts": [{{"concept": "string", "definition": "string"}}],
  "mnemonics": ["string"]
}}

Rules:
- summary: {summary_instruction}
- keywords: 8–12 concise, topic-relevant keywords or key phrases.
- questions: Exactly {num_questions} meaningful, thought-provoking revision questions.
- topic: One short phrase identifying the subject area (e.g. "Cell Biology", "World War II", "Thermodynamics").
- difficulty: Assess the material difficulty as "Easy", "Medium", or "Hard".
- key_concepts: 3–5 core concepts from the notes, each with a brief definition (1–2 sentences).
- mnemonics: 1–3 creative memory aids, acronyms, or mnemonic devices to help remember key ideas. If none apply naturally, return an empty list.
- Return ONLY the JSON object. No markdown, no extra text.

Notes:
\"\"\"
{text}
\"\"\"
"""


def _clean_json_response(raw: str) -> str:
    raw = re.sub(r"```(?:json)?\s*", "", raw)
    return raw.replace("```", "").strip()


def _parse_response(raw: str) -> dict:
    cleaned = _clean_json_response(raw)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group())
            except json.JSONDecodeError:
                raise ValueError("Gemini returned malformed JSON that could not be recovered.")
        else:
            raise ValueError("Gemini response did not contain a recognisable JSON object.")

    # Validate required fields
    missing = EXPECTED_KEYS - set(data.keys())
    if missing:
        raise ValueError(f"Gemini response missing required fields: {missing}")

    # Normalise types
    if isinstance(data.get("keywords"), str):
        data["keywords"] = [k.strip() for k in data["keywords"].split(",")]
    if isinstance(data.get("questions"), str):
        data["questions"] = [data["questions"]]

    # Provide defaults for optional fields
    data.setdefault("topic", "General")
    data.setdefault("difficulty", "Medium")
    data.setdefault("key_concepts", [])
    data.setdefault("mnemonics", [])

    return data


def configure_gemini(api_key: str) -> None:
    genai.configure(api_key=api_key)


def analyze_text(
    text: str,
    api_key: Optional[str] = None,
    summary_length: str = "Medium",
    num_questions: int = 5,
    model_name: str = "gemini-3-flash-preview",
) -> dict:
    """
    Analyse cleaned notes text with Gemini.

    Returns dict with keys:
        summary, keywords, questions, topic, difficulty, key_concepts, mnemonics
    """
    resolved_key = api_key or os.getenv("GEMINI_API_KEY", "")
    if not resolved_key:
        raise ValueError(
            "Gemini API key is missing. Add it to the sidebar or set GEMINI_API_KEY in your .env."
        )

    configure_gemini(resolved_key)
    prompt = _build_prompt(text, summary_length, num_questions)

    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        raw_text = response.text
    except Exception as e:
        raise RuntimeError(f"Gemini API call failed: {e}") from e

    return _parse_response(raw_text)
