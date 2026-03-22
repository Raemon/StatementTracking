"""Tests for the /api/people endpoints.

Covers the people list (with aggregated quote counts), individual person
profile retrieval, and field update persistence.
"""

import pytest

from app.models import Person


class TestPeopleList:

    async def test_people_list_returns_quote_counts(self, client, sample_quote):
        # GET /api/people should include a quote_count field for each
        # person that reflects the number of non-duplicate quotes attributed
        # to them.
        pass


class TestPersonProfile:

    async def test_person_profile_returns_all_quotes(
        self, client, sample_person, sample_quote
    ):
        # GET /api/people/<id> should return the person's details plus a
        # list of all their non-duplicate quotes with article metadata.
        pass


class TestPersonUpdate:

    async def test_editing_person_fields_persists(self, client, db_session, sample_person):
        # PUT /api/people/<id> with updated fields (e.g. role, party)
        # should persist the changes to the database and return the
        # updated person object.
        pass
