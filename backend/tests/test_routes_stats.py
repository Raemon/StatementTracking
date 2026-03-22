"""Tests for the /api/stats endpoint.

Covers aggregate statistics: total counts, quotes grouped by month, and
quotes grouped by party.
"""

import pytest


class TestStats:

    async def test_stats_returns_correct_total_counts(self, client, sample_quote):
        # GET /api/stats should return total_quotes and total_people that
        # match the number of non-duplicate quotes and people in the database.
        pass

    async def test_quotes_per_month_grouping(
        self, client, db_session, sample_person, sample_article
    ):
        # quotes_over_time should group quotes by their date_said month
        # in YYYY-MM format, with accurate counts per bucket.
        pass

    async def test_quotes_by_party_grouping(self, client, sample_quote):
        # quotes_by_party should return one entry per party with the count
        # of non-duplicate quotes attributed to people of that party.
        pass
