"""Tests for article/PDF fetching."""

from unittest.mock import MagicMock, patch

import pytest

from app.services.fetcher import (
    FetchError,
    _fetch_pdf_article,
    _is_pdf_url,
    fetch_article,
)


class TestIsPdfUrl:
    def test_https_path_ending_pdf(self):
        assert _is_pdf_url("https://gov.example/reports/hearing.pdf") is True

    def test_case_insensitive_extension(self):
        assert _is_pdf_url("https://x.org/doc.PDF") is True

    def test_not_pdf(self):
        assert _is_pdf_url("https://news.example/article") is False


class TestFetchPdfArticle:
    @patch("app.services.fetcher.httpx.Client")
    def test_invalid_magic_raises(self, mock_client_cls):
        mock_response = MagicMock()
        mock_response.content = b"not a pdf file"
        mock_response.raise_for_status = MagicMock()
        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client_cls.return_value = mock_client

        with pytest.raises(FetchError, match="%PDF"):
            _fetch_pdf_article("https://example.com/x.pdf")

    @patch("app.services.fetcher.httpx.Client")
    def test_extracts_text_and_title(self, mock_client_cls):
        pdf_bytes = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"
        mock_response = MagicMock()
        mock_response.content = pdf_bytes
        mock_response.raise_for_status = MagicMock()
        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client_cls.return_value = mock_client

        mock_page = MagicMock()
        mock_page.extract_text.return_value = "x" * 120
        mock_reader = MagicMock()
        mock_reader.pages = [mock_page]
        mock_reader.metadata = None
        mock_reader.is_encrypted = False

        with patch("app.services.fetcher.PdfReader", return_value=mock_reader):
            out = _fetch_pdf_article("https://example.com/doc.pdf")

        assert out["url"] == "https://example.com/doc.pdf"
        assert len(out["text"]) >= 100
        assert out["title"] is None
        assert out["publication"] == "Example"


class TestFetchArticleRoutesToPdf:
    @patch("app.services.fetcher._fetch_pdf_article")
    def test_pdf_url_uses_pdf_branch(self, mock_pdf):
        mock_pdf.return_value = {
            "title": "T",
            "text": "y" * 100,
            "publication": "P",
            "published_date": None,
            "url": "https://a.com/x.pdf",
        }
        fetch_article("https://a.com/x.pdf")
        mock_pdf.assert_called_once_with("https://a.com/x.pdf")
