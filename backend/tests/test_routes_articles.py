"""Tests for the /api/articles endpoints.

Covers article URL submission (extract), duplicate detection on save, and
the creation of article / person / quote records during the save workflow.
"""

import pytest

from app.models import Article, Person, Quote


class TestArticlesExtract:

    async def test_extract_returns_expected_structure(self, client, mock_anthropic):
        # POST /api/articles/extract with a valid URL should return an
        # ExtractResponse containing article metadata and a quotes list,
        # without persisting anything to the database.
        pass


class TestArticlesSave:

    async def test_duplicate_url_returns_existing_article(self, client, db_session, sample_article):
        # POST /api/articles/save with a URL that already exists in the
        # database should attach new quotes to the existing article record
        # rather than creating a duplicate.
        pass

    async def test_save_creates_article_people_and_quotes(self, client, db_session, sample_person):
        # A successful save should create one Article row, link to the
        # provided person_id, and create the correct number of Quote rows.
        pass

    async def test_save_with_new_person_creates_person_record(self, client, db_session):
        # When a quote includes new_person instead of person_id, the save
        # endpoint should create a new Person row and link the quote to it.
        pass
