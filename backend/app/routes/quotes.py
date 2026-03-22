from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..models import Quote, Person, Article
from ..schemas import QuoteUpdate

router = APIRouter(prefix="/api/quotes", tags=["quotes"])


def _quote_to_dict(q: Quote) -> dict:
    return {
        "id": q.id,
        "quote_text": q.quote_text,
        "context": q.context,
        "date_said": q.date_said.isoformat() if q.date_said else None,
        "created_at": q.created_at.isoformat() if q.created_at else None,
        "person": {
            "id": q.person.id,
            "name": q.person.name,
            "type": q.person.type.value if q.person.type else None,
            "party": q.person.party.value if q.person.party else None,
            "role": q.person.role,
            "chamber": q.person.chamber.value if q.person.chamber else None,
            "state": q.person.state,
            "employer": q.person.employer,
        } if q.person else None,
        "article": {
            "id": q.article.id,
            "url": q.article.url,
            "title": q.article.title,
            "publication": q.article.publication,
            "published_date": (
                q.article.published_date.isoformat()
                if q.article.published_date
                else None
            ),
        } if q.article else None,
    }


@router.get("")
def list_quotes(
    person_id: Optional[int] = None,
    search: Optional[str] = None,
    party: Optional[str] = None,
    type: Optional[str] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    query = (
        db.query(Quote)
        .options(joinedload(Quote.person), joinedload(Quote.article))
    )

    if person_id:
        query = query.filter(Quote.person_id == person_id)
    if search:
        query = query.filter(Quote.quote_text.ilike(f"%{search}%"))
    if party:
        query = query.join(Person).filter(Person.party == party)
    if type:
        if not party:
            query = query.join(Person)
        query = query.filter(Person.type == type)
    if from_date:
        query = query.filter(Quote.date_said >= from_date)
    if to_date:
        query = query.filter(Quote.date_said <= to_date)

    total = query.count()

    quotes = (
        query.order_by(Quote.date_said.desc().nullslast(), Quote.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return {
        "quotes": [_quote_to_dict(q) for q in quotes],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get("/{quote_id}")
def get_quote(quote_id: int, db: Session = Depends(get_db)):
    quote = (
        db.query(Quote)
        .options(joinedload(Quote.person), joinedload(Quote.article))
        .filter(Quote.id == quote_id)
        .first()
    )
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found.")
    return _quote_to_dict(quote)


@router.put("/{quote_id}")
def update_quote(
    quote_id: int, updates: QuoteUpdate, db: Session = Depends(get_db)
):
    quote = db.query(Quote).filter(Quote.id == quote_id).first()
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found.")

    update_data = updates.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(quote, field, value)

    db.commit()
    db.refresh(quote)

    loaded = (
        db.query(Quote)
        .options(joinedload(Quote.person), joinedload(Quote.article))
        .filter(Quote.id == quote_id)
        .first()
    )
    return _quote_to_dict(loaded)


@router.delete("/{quote_id}")
def delete_quote(quote_id: int, db: Session = Depends(get_db)):
    quote = db.query(Quote).filter(Quote.id == quote_id).first()
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found.")
    db.delete(quote)
    db.commit()
    return {"ok": True}
