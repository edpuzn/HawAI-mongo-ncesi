from __future__ import annotations
from typing import Tuple

# Minimal rule-based red flag phrases in Turkish
RED_FLAG_TERMS: tuple[str, ...] = (
    "gogus agrisi",
    "göğüs ağrısı",
    "şiddetli baş ağrısı",
    "siddetli bas agrisi",
    "nefes darlığı",
    "nefes darligi",
    "bilinç kaybı",
    "bilinc kaybi",
    "felç",
    "inme",
    "kontrol edilemeyen kanama",
    "yüksek ateş",
    "yuksek ates",
    "şiddetli karın ağrısı",
    "siddetli karin agrisi",
)

EMERGENCY_SUFFIX = (
    "\n\nACIL UYARI: Belirtiler acil durum olabilir. 112'yi arayın veya en yakın acil servise başvurun."
)


def detect_red_flag(text: str) -> bool:
    t = text.lower()
    return any(term in t for term in RED_FLAG_TERMS)


def append_emergency_notice(reply: str) -> str:
    if reply.strip().endswith(EMERGENCY_SUFFIX.strip()):
        return reply
    return f"{reply}{EMERGENCY_SUFFIX}"
