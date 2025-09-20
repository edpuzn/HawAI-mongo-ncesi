from __future__ import annotations
from typing import List


RULES = {
    "3.3": [
        "enfeksiyon",
        "hiv",
        "aids",
        "tüberküloz",
        "tuberkuloz",
        "sıtma",
        "malarya",
        "hepatit",
    ],
    "3.4": [
        "ruh",
        "psikoloji",
        "depresyon",
        "anksiyete",
        "intihar",
        "kalp",
        "kanser",
        "obezite",
        "diyabet",
    ],
    "3.b": [
        "aşı",
        "asi",
        "ilaç",
        "ilac",
        "ar-ge",
        "arge",
        "arastirma",
        "klinik",
        "deney",
    ],
    "3.9": [
        "kirlilik",
        "hava",
        "su",
        "kimyasal",
        "zehirlenme",
        "asbest",
        "kurşun",
        "kursun",
    ],
}


def classify_sdg_tags(text: str) -> List[str]:
    t = text.lower()
    tags: List[str] = []
    for tag, keywords in RULES.items():
        if any(k in t for k in keywords):
            tags.append(tag)
    if not tags:
        tags = ["3.x"]
    return sorted(set(tags))
