"""
Session history service — persists analysis results to a local JSON file.
Each session is stored with a timestamp, topic, summary preview, and full result.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional
import uuid

DATA_DIR = Path(__file__).parent.parent / "data"
HISTORY_FILE = DATA_DIR / "history.json"
MAX_SESSIONS = 50  # Keep the last 50 sessions


def _load_raw() -> list[dict]:
    """Load the history file, returning [] on any error."""
    try:
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
    except Exception:
        pass
    return []


def _save_raw(sessions: list[dict]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(sessions, f, ensure_ascii=False, indent=2)


def save_session(
    result: dict,
    ocr_text: str,
    input_mode: str,
    summary_length: str,
    num_questions: int,
    image_name: Optional[str] = None,
) -> str:
    """
    Persist one analysis session.
    Returns the session ID.
    """
    sessions = _load_raw()

    session_id = str(uuid.uuid4())[:8]
    session = {
        "id":             session_id,
        "timestamp":      datetime.now().isoformat(),
        "input_mode":     input_mode,
        "image_name":     image_name or "",
        "summary_length": summary_length,
        "num_questions":  num_questions,
        "topic":          result.get("topic", "General"),
        "difficulty":     result.get("difficulty", "Medium"),
        "ocr_text":       ocr_text,
        "result":         result,
    }

    sessions.insert(0, session)
    sessions = sessions[:MAX_SESSIONS]
    _save_raw(sessions)
    return session_id


def load_history() -> list[dict]:
    """Return all saved sessions, newest first."""
    return _load_raw()


def get_session(session_id: str) -> Optional[dict]:
    """Return a single session by ID, or None if not found."""
    for s in _load_raw():
        if s.get("id") == session_id:
            return s
    return None


def delete_session(session_id: str) -> bool:
    """Delete a session by ID. Returns True if found and deleted."""
    sessions = _load_raw()
    before = len(sessions)
    sessions = [s for s in sessions if s.get("id") != session_id]
    if len(sessions) < before:
        _save_raw(sessions)
        return True
    return False


def clear_history() -> None:
    """Delete all saved sessions."""
    _save_raw([])


def format_timestamp(iso: str) -> str:
    """Convert ISO timestamp to a human-readable string."""
    try:
        dt = datetime.fromisoformat(iso)
        return dt.strftime("%d %b %Y, %I:%M %p")
    except Exception:
        return iso
