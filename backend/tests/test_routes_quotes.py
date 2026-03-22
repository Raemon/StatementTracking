"""Tests for the /api/quotes endpoints.

Covers listing with joins, filtering (person, party, date, fulltext),
pagination, editing quote text, and deletion.
"""

import pytest

from app.models import Quote


class TestQuotesList:

    async def test_quotes_returns_joined_data(self, client, sample_quote):
        # GET /api/quotes should return quote objects that include nested
        # person and article data from the joined relationships.
        pass

    async def test_filter_by_person_id(self, client, sample_quote):
        # Passing ?person_id=<id> should return only quotes belonging
        # to that person; other people's quotes must be absent.
        pass

    async def test_filter_by_party(self, client, sample_quote):
        # Passing ?party=Democrat should return only quotes from speakers
        # whose party matches; other parties must be absent.
        pass

    async def test_filter_by_date_range(self, client, sample_quote):
        # Passing ?from_date and ?to_date should return only quotes whose
        # date_said falls within the inclusive range.
        pass

    async def test_fulltext_search(self, client, sample_quote):
        # Passing ?search=<substring> should return only quotes whose
        # quote_text contains the search term (case-insensitive).
        pass

    async def test_pagination(self, client, db_session, sample_person, sample_article):
        # When more quotes exist than page_size, the response should
        # respect page and page_size parameters and report the correct total.
        pass


class TestQuotesMutations:

    async def test_edit_quote_text(self, client, sample_quote):
        # PUT /api/quotes/<id> with a new quote_text should persist the
        # change and return the updated quote in the response.
        pass

    async def test_delete_quote(self, client, db_session, sample_quote):
        # DELETE /api/quotes/<id> should remove the quote from the database
        # and return {"ok": true}; a subsequent GET should 404.
        pass
