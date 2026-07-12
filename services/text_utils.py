"""
Text cleaning and preparation utilities.
Used between OCR output and Gemini input.
"""

import re


# Max characters sent to Gemini to stay within safe prompt limits
MAX_TEXT_LENGTH = 8000


def remove_null_characters(text: str) -> str:
    """Strip null bytes that occasionally appear in OCR output."""
    return text.replace("\x00", "")


def normalize_whitespace(text: str) -> str:
    """Collapse repeated spaces and tabs into a single space."""
    return re.sub(r"[ \t]+", " ", text)


def normalize_line_breaks(text: str) -> str:
    """Collapse 3+ consecutive newlines into a maximum of two."""
    return re.sub(r"\n{3,}", "\n\n", text)


def strip_leading_trailing(text: str) -> str:
    """Remove leading/trailing whitespace from each line and the whole text."""
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(lines).strip()


def safe_truncate(text: str, max_length: int = MAX_TEXT_LENGTH) -> str:
    """
    Truncate text at a word boundary to avoid cutting mid-sentence.
    Adds a note when truncation occurs.
    """
    if len(text) <= max_length:
        return text

    truncated = text[:max_length].rsplit(" ", 1)[0]
    return truncated + "\n\n[Note: Text was truncated to fit prompt limits.]"


def clean_text(text: str, truncate: bool = True) -> str:
    """
    Full cleaning pipeline: null removal → whitespace → line breaks → strip → truncate.
    Returns cleaned text ready for Gemini.
    """
    text = remove_null_characters(text)
    text = normalize_whitespace(text)
    text = normalize_line_breaks(text)
    text = strip_leading_trailing(text)
    if truncate:
        text = safe_truncate(text)
    return text


def is_meaningful_text(text: str, min_words: int = 5) -> bool:
    """
    Check whether extracted text has enough content to analyze.
    Returns False for blank or near-blank OCR results.
    """
    words = text.split()
    return len(words) >= min_words
