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


# Simple identity override to ensure consistent branding and safety notice
_IDENTITY_TRIGGERS: tuple[str, ...] = (
    "sen kimsin",
    "kimsin",
    "kimsiniz",
    "adın ne",
    "adin ne",
    "kendini tanıt",
    "kendini tanit",
    "kim olduğunu",
    "kim oldugunu",
    "ne için özelleştirildin",
    "ne icin ozellestirildin",
)

_IDENTITY_REPLY = (
    "Ben HawAI’yim: Türkiye odaklı, güvenli ve kanıta dayalı yardımcı sağlık rehberi. "
    "SDG-3 kapsamındaki konularda bilgi amaçlı rehberlik sağlarım; teşhis veya tedavi önerisi veremem. "
    "Acil durumda 112’yi arayın."
)


def override_identity_if_needed(user_message: str, reply: str) -> str:
    text = (user_message or "").strip().lower()
    if any(trigger in text for trigger in _IDENTITY_TRIGGERS):
        return _IDENTITY_REPLY
    return reply
