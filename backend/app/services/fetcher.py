import io
from datetime import date
from typing import Optional
from urllib.parse import urlparse

import httpx
from newspaper import Article, ArticleException
from pypdf import PdfReader
from pypdf.errors import PdfReadError

PUBLICATION_LOOKUP = {
    "nytimes.com": "The New York Times",
    "washingtonpost.com": "The Washington Post",
    "wsj.com": "The Wall Street Journal",
    "politico.com": "Politico",
    "thehill.com": "The Hill",
    "reuters.com": "Reuters",
    "apnews.com": "Associated Press",
    "cnn.com": "CNN",
    "foxnews.com": "Fox News",
    "nbcnews.com": "NBC News",
    "abcnews.go.com": "ABC News",
    "cbsnews.com": "CBS News",
    "bbc.com": "BBC",
    "bbc.co.uk": "BBC",
    "theguardian.com": "The Guardian",
    "axios.com": "Axios",
    "bloomberg.com": "Bloomberg",
    "techcrunch.com": "TechCrunch",
    "wired.com": "Wired",
    "theverge.com": "The Verge",
    "arstechnica.com": "Ars Technica",
    "npr.org": "NPR",
    "pbs.org": "PBS",
    "usatoday.com": "USA Today",
    "latimes.com": "Los Angeles Times",
    "cnbc.com": "CNBC",
    "ft.com": "Financial Times",
}


def _derive_publication(url: str) -> str:
    hostname = urlparse(url).hostname or ""
    hostname = hostname.removeprefix("www.")
    if hostname in PUBLICATION_LOOKUP:
        return PUBLICATION_LOOKUP[hostname]
    parts = hostname.rsplit(".", 2)
    if len(parts) >= 2:
        return parts[-2].capitalize()
    return hostname


def _parse_publish_date(article: Article) -> Optional[date]:
    if article.publish_date:
        if hasattr(article.publish_date, "date"):
            return article.publish_date.date()
        if isinstance(article.publish_date, date):
            return article.publish_date
    return None


class FetchError(Exception):
    pass


def _is_pdf_url(url: str) -> bool:
    try:
        path = (urlparse(url.strip()).path or "").lower()
    except Exception:
        return False
    if not path:
        return False
    return path.rsplit("/", 1)[-1].endswith(".pdf")


def _pdf_metadata_title(reader: PdfReader) -> Optional[str]:
    meta = reader.metadata
    if not meta:
        return None
    title = getattr(meta, "title", None)
    if title:
        return str(title).strip() or None
    if hasattr(meta, "get"):
        raw = meta.get("/Title")
        if raw:
            return str(raw).strip() or None
    return None


def _fetch_pdf_article(url: str) -> dict:
    headers = {
        "User-Agent": (
            "StatementTracking/1.0 (+https://github.com/) article-extractor"
        ),
        "Accept": "application/pdf,*/*;q=0.8",
    }
    try:
        with httpx.Client(timeout=60.0, follow_redirects=True) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            data = response.content
    except httpx.HTTPError as e:
        raise FetchError(f"Failed to download PDF: {e}") from e

    if len(data) < 5 or not data[:5].startswith(b"%PDF-"):
        raise FetchError(
            "The URL did not return a valid PDF file (missing %PDF header)."
        )

    try:
        reader = PdfReader(io.BytesIO(data))
    except PdfReadError as e:
        raise FetchError(f"Could not read PDF: {e}") from e

    if getattr(reader, "is_encrypted", False):
        raise FetchError(
            "PDF is password-protected or encrypted and cannot be extracted."
        )

    text_parts: list[str] = []
    for page in reader.pages:
        try:
            text_parts.append(page.extract_text() or "")
        except Exception as e:
            raise FetchError(f"Failed to extract text from PDF page: {e}") from e

    text = "\n".join(text_parts).strip()

    if not text or len(text) < 100:
        raise FetchError(
            "Extracted PDF text is too short or empty — the file may be "
            "image-only (scanned) or protected."
        )

    title = _pdf_metadata_title(reader)

    return {
        "title": title,
        "text": text,
        "publication": _derive_publication(url),
        "published_date": None,
        "url": url,
    }


def fetch_article(url: str) -> dict:
    if _is_pdf_url(url):
        return _fetch_pdf_article(url)

    try:
        article = Article(url)
        article.download()
        article.parse()
    except ArticleException as e:
        raise FetchError(f"Failed to fetch article: {e}")
    except Exception as e:
        raise FetchError(f"Unexpected error fetching article: {e}")

    if not article.text or len(article.text.strip()) < 100:
        raise FetchError(
            "Article text is too short or empty — the page may be behind a paywall "
            "or require JavaScript rendering."
        )

    return {
        "title": article.title or None,
        "text": article.text,
        "publication": _derive_publication(url),
        "published_date": _parse_publish_date(article),
        "url": url,
    }
