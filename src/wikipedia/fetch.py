"""
Lấy wikitext từ bài viết Wikipedia (MediaWiki REST API).
Hỗ trợ mọi phiên bản ngôn ngữ (en, vi, fr, ...).
Tham chiếu: docs/nghien-cuu.md § 3.
"""
from urllib.parse import urlparse, unquote
import requests

DEFAULT_USER_AGENT = "WikipediaTranslator/1.0 (https://github.com/; Python)"
WIKI_REST_URL = "https://en.wikipedia.org/w/rest.php/v1/page"


def parse_url_to_title(url: str) -> str:
    """
    Từ URL bài viết Wikipedia, trích title dùng cho API.
    Ví dụ: https://en.wikipedia.org/wiki/Front-side_bus -> Front-side_bus
    """
    _, title = parse_url_to_base_and_title(url)
    return title


def parse_url_to_base_and_title(url: str) -> tuple[str, str]:
    """
    Từ URL bài viết Wikipedia, trả về (rest_base_url, title).
    rest_base_url dùng cho REST API (vd: https://en.wikipedia.org/w/rest.php/v1/page).
    """
    url = (url or "").strip()
    if not url:
        raise ValueError("URL trống")
    parsed = urlparse(url)
    base = f"{parsed.scheme or 'https'}://{parsed.netloc}"
    path = parsed.path.rstrip("/")
    if "/wiki/" not in path:
        raise ValueError("URL không phải dạng Wikipedia /wiki/...")
    title = path.split("/wiki/", 1)[-1]
    if not title:
        raise ValueError("Không tìm thấy title trong URL")
    title = title.split("?")[0].split("#")[0].strip()
    title = unquote(title)
    if " " in title:
        title = title.replace(" ", "_")
    rest_base = f"{base.rstrip('/')}/w/rest.php/v1/page"
    return rest_base, title


def fetch_wikitext(
    title: str,
    *,
    user_agent: str = DEFAULT_USER_AGENT,
    base_url: str = WIKI_REST_URL,
) -> str:
    """
    GET REST API Wikipedia, trả về wikitext (source).
    Raise requests.RequestException hoặc ValueError nếu lỗi.
    """
    title = (title or "").strip().replace(" ", "_")
    if not title:
        raise ValueError("Title trống")
    url = f"{base_url.rstrip('/')}/{title}"
    headers = {"User-Agent": user_agent}
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if "source" not in data:
        raise ValueError("API không trả về trường 'source'")
    return data["source"]


def fetch_wikitext_from_url(
    url: str,
    *,
    user_agent: str = DEFAULT_USER_AGENT,
) -> str:
    """
    Từ URL bài viết Wikipedia (bất kỳ ngôn ngữ), parse base + title rồi gọi API lấy wikitext.
    """
    rest_base, title = parse_url_to_base_and_title(url)
    return fetch_wikitext(title, user_agent=user_agent, base_url=rest_base)
