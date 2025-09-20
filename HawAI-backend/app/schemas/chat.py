from __future__ import annotations
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class ChatIn(BaseModel):
    message: str
    user_meta: Optional[Dict[str, object]] = Field(default_factory=dict)


class Source(BaseModel):
    title: str
    url: str


class Safety(BaseModel):
    is_emergency: bool


class ChatOut(BaseModel):
    reply: str
    sdg_tags: List[str]
    sources: List[Source]
    safety: Safety
