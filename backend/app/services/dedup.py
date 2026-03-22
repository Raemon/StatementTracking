import re
import unicodedata
from typing import Optional

from sqlalchemy.orm import Session

from ..models import Quote


def normalize_text(text: str) -> str:
    """Collapse a quote to a canonical form for comparison.

    Strips quotes/punctuation, collapses whitespace, lowercases, and removes
    diacritics so that minor transcription differences don't prevent matching.
    """
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def find_duplicate(
    db: Session,
    person_id: int,
    quote_text: str,
    exclude_quote_id: Optional[int] = None,
) -> Optional[Quote]:
    """Return the first existing quote that is a duplicate of the given text.

    A quote is a duplicate when either:
    - normalized texts match exactly, or
    - one is a substantial substring of the other (>=80% of the shorter text)
    """
    normalized = normalize_text(quote_text)
    if not normalized:
        return None

    existing_quotes = (
        db.query(Quote)
        .filter(Quote.person_id == person_id)
        .filter(Quote.is_duplicate == False)  # noqa: E712
    )
    if exclude_quote_id:
        existing_quotes = existing_quotes.filter(Quote.id != exclude_quote_id)

    for existing in existing_quotes.all():
        existing_norm = normalize_text(existing.quote_text)
        if not existing_norm:
            continue

        if normalized == existing_norm:
            return existing

        shorter = min(len(normalized), len(existing_norm))
        if shorter < 20:
            continue
        if normalized in existing_norm or existing_norm in normalized:
            overlap_ratio = shorter / max(len(normalized), len(existing_norm))
            if overlap_ratio >= 0.8:
                return existing

    return None


def check_duplicates_batch(
    db: Session,
    items: list[dict],
) -> list[dict]:
    """Check a batch of {speaker_name, quote_text} items against the DB.

    Returns a list with the same length, each element containing:
      - is_duplicate: bool
      - existing_quote: dict | None  (id, quote_text, article title/url)
    """
    from ..models import Person

    results = []
    for item in items:
        speaker_name = (item.get("speaker_name") or "").strip().lower()
        quote_text = item.get("quote_text", "")

        if not speaker_name or not quote_text:
            results.append({"is_duplicate": False, "existing_quote": None})
            continue

        person = db.query(Person).filter(Person.name.ilike(speaker_name)).first()
        if not person:
            results.append({"is_duplicate": False, "existing_quote": None})
            continue

        dup = find_duplicate(db, person.id, quote_text)
        if dup:
            results.append({
                "is_duplicate": True,
                "existing_quote": {
                    "id": dup.id,
                    "quote_text": dup.quote_text[:200],
                    "article_title": dup.article.title if dup.article else None,
                    "article_url": dup.article.url if dup.article else None,
                },
            })
        else:
            results.append({"is_duplicate": False, "existing_quote": None})

    return results
