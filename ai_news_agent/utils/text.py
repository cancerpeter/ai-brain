from __future__ import annotations

import hashlib
import html
import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime


WHITESPACE_RE = re.compile(r"\s+")
TAG_RE = re.compile(r"<[^>]+>")


def normalize_whitespace(value: str) -> str:
    return WHITESPACE_RE.sub(" ", value or "").strip()


def strip_html(value: str) -> str:
    text = TAG_RE.sub(" ", value or "")
    return normalize_whitespace(html.unescape(text))


def title_hash(title: str) -> str:
    normalized = normalize_whitespace(title).lower()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def parse_datetime_to_iso(value: str) -> str:
    raw = normalize_whitespace(value)
    if not raw:
        return ""

    candidates = (
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%b %d, %Y",
        "%B %d, %Y",
    )

    for fmt in candidates:
        try:
            parsed = datetime.strptime(raw, fmt)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed.astimezone(timezone.utc).isoformat()
        except ValueError:
            continue

    try:
        parsed = parsedate_to_datetime(raw)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc).isoformat()
    except (TypeError, ValueError, IndexError):
        return raw


def truncate_text(value: str, limit: int = 220) -> str:
    text = normalize_whitespace(value)
    if len(text) <= limit:
        return text
    return f"{text[: limit - 3].rstrip()}..."

