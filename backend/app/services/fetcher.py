from datetime import date
from typing import Optional
from urllib.parse import urlparse

from newspaper import Article, ArticleException

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


def fetch_article(url: str) -> dict:
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
