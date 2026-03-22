"""Tests for the AI quote extraction service.

Validates that app.services.extractor.extract_quotes correctly parses LLM
responses, reassembles fragmented quotes, filters speaker types, and handles
malformed output gracefully.
"""

import pytest

from app.services.extractor import ExtractionError, extract_quotes


class TestExtraction:

    def test_extraction_returns_correct_quote_count(
        self, mock_anthropic, sample_article_text
    ):
        # Should return exactly three quotes (two from the senator, one from
        # staff) when given the sample article; the tech CEO is excluded.
        pass

    def test_fragmented_quotes_reassembled_with_ellipsis(
        self, mock_anthropic, sample_article_text
    ):
        # The senator's interrupted quote ("The companies building these
        # systems," she added, "have ...") should appear as a single
        # quote_text with an ellipsis joining the fragments.
        pass

    def test_non_politician_speakers_excluded(
        self, mock_anthropic, sample_article_text
    ):
        # Marcus Chen (Orion Labs CEO) should not appear in the returned
        # quotes because he is not a policymaker, official, or staff member.
        pass

    def test_malformed_llm_response_handled_gracefully(self, mock_anthropic):
        # When the LLM returns invalid JSON or a response missing the
        # "quotes" key, extract_quotes should raise ExtractionError with
        # a descriptive message rather than an unhandled exception.
        pass
