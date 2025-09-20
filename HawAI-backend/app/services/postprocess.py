from __future__ import annotations
from typing import List
from app.core.redflags import detect_red_flag, append_emergency_notice


def build_sources() -> List[dict]:
    return [
        {"title": "World Health Organization (WHO)", "url": "https://www.who.int/"},
        {"title": "United Nations SDG 3", "url": "https://sdgs.un.org/goals/goal3"},
    ]


def apply_emergency_if_needed(user_message: str, reply: str) -> tuple[str, bool]:
    is_emergency = detect_red_flag(user_message)
    if is_emergency:
        reply = append_emergency_notice(reply)
    return reply, is_emergency
