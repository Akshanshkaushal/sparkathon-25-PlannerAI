from __future__ import annotations

import html
import logging
import re
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote_plus

import requests
from langchain_core.tools import tool

from app.services.walmart_service import search_walmart_product

logger = logging.getLogger(__name__)


FALLBACK_CATALOG = {
    "books": [
        {"title": "Kindle Paperwhite", "price": 149.99, "link": "https://www.amazon.com/s?k=Kindle+Paperwhite"},
        {"title": "Personalized book embosser", "price": 29.99, "link": "https://www.etsy.com/search?q=personalized+book+embosser"},
        {"title": "Premium reading light", "price": 18.99, "link": "https://www.walmart.com/search?q=premium+reading+light"},
    ],
    "gadgets": [
        {"title": "Anker portable charger", "price": 39.99, "link": "https://www.walmart.com/search?q=anker+portable+charger"},
        {"title": "Bluetooth item tracker", "price": 24.99, "link": "https://www.walmart.com/search?q=bluetooth+item+tracker"},
        {"title": "Smart speaker", "price": 49.99, "link": "https://www.walmart.com/search?q=smart+speaker"},
    ],
    "travel": [
        {"title": "Carry-on packing cubes", "price": 21.99, "link": "https://www.walmart.com/search?q=packing+cubes"},
        {"title": "Travel neck pillow", "price": 19.99, "link": "https://www.walmart.com/search?q=travel+neck+pillow"},
        {"title": "Universal travel adapter", "price": 22.99, "link": "https://www.walmart.com/search?q=universal+travel+adapter"},
    ],
    "cooking": [
        {"title": "Digital meat thermometer", "price": 16.99, "link": "https://www.walmart.com/search?q=digital+meat+thermometer"},
        {"title": "Chef knife", "price": 34.99, "link": "https://www.walmart.com/search?q=chef+knife"},
        {"title": "Spice rack organizer", "price": 27.99, "link": "https://www.walmart.com/search?q=spice+rack+organizer"},
    ],
    "decorations": [
        {"title": "Birthday decoration kit", "price": 24.99, "link": "https://www.walmart.com/search?q=birthday+decoration+kit"},
        {"title": "Warm white string lights", "price": 12.99, "link": "https://www.walmart.com/search?q=warm+white+string+lights"},
        {"title": "Balloon arch kit", "price": 18.99, "link": "https://www.walmart.com/search?q=balloon+arch+kit"},
    ],
    "cake": [
        {"title": "Custom birthday cake order", "price": 45.0, "link": "https://www.walmart.com/cp/bakery-cakes/976779"},
        {"title": "Chocolate celebration cake", "price": 28.0, "link": "https://www.walmart.com/search?q=chocolate+birthday+cake"},
    ],
}


@dataclass
class ProductCandidate:
    source: str
    title: str
    price: float
    currency: str = "$"
    link: str = ""
    image: str | None = None
    reviews_count: str = "N/A"
    is_best_seller: bool = False
    rationale: str = ""

    def to_cart_item(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "title": self.title,
            "image": self.image,
            "link": self.link,
            "price": {
                "currentPrice": f"{self.price:.2f}",
                "currency": self.currency,
            },
            "reviewsCount": self.reviews_count,
            "isBestSeller": self.is_best_seller,
            "rationale": self.rationale,
        }


def _parse_price(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    match = re.search(r"\d+(?:\.\d+)?", str(value).replace(",", ""))
    return float(match.group(0)) if match else None


def _from_walmart_product(product: dict[str, Any]) -> ProductCandidate | None:
    price_info = product.get("price", {})
    price = _parse_price(price_info.get("currentPrice"))
    title = product.get("title")
    if not title or price is None:
        return None

    return ProductCandidate(
        source=product.get("source", "Walmart API"),
        title=title,
        image=product.get("image"),
        link=product.get("link") or f"https://www.walmart.com/search?q={quote_plus(title)}",
        price=price,
        currency=price_info.get("currency", "$"),
        reviews_count=str(product.get("reviewsCount") or "N/A"),
        is_best_seller=bool(product.get("isBestSeller", False)),
    )


def _search_duckduckgo(query: str, limit: int = 5) -> list[ProductCandidate]:
    url = "https://html.duckduckgo.com/html/"
    try:
        response = requests.get(url, params={"q": f"{query} buy price"}, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        logger.info("DuckDuckGo fallback search failed for query '%s'", query, exc_info=True)
        return []

    candidates: list[ProductCandidate] = []
    result_pattern = re.compile(
        r'<a rel="nofollow" class="result__a" href="(?P<link>.*?)">(?P<title>.*?)</a>',
        re.IGNORECASE | re.DOTALL,
    )
    for match in result_pattern.finditer(response.text):
        title = re.sub(r"<.*?>", "", html.unescape(match.group("title"))).strip()
        link = html.unescape(match.group("link"))
        if not title:
            continue
        candidates.append(
            ProductCandidate(
                source="Web Search",
                title=title,
                price=0.0,
                link=link,
                rationale="Discovered from web search; price needs retailer verification.",
            )
        )
        if len(candidates) >= limit:
            break
    return candidates


def _fallback_candidates(query: str, category: str) -> list[ProductCandidate]:
    if category.lower() in {"decorations", "cake"}:
        matched_key = category.lower()
    else:
        lookup_text = f"{query} {category}".lower()
        matched_key = next((key for key in FALLBACK_CATALOG if key in lookup_text), category.lower())
    items = FALLBACK_CATALOG.get(matched_key) or FALLBACK_CATALOG.get("gadgets", [])
    return [
        ProductCandidate(
            source="Curated Fallback Catalog",
            title=item["title"],
            price=float(item["price"]),
            link=item["link"],
            rationale="Used when live shopping APIs do not return enough products.",
        )
        for item in items
    ]


def discover_products(query: str, category: str, limit: int = 6) -> list[ProductCandidate]:
    """Search retailer and web sources, normalize, and deduplicate candidates."""
    candidates: list[ProductCandidate] = []

    for product in search_walmart_product(query):
        candidate = _from_walmart_product(product)
        if candidate:
            candidates.append(candidate)

    if len(candidates) < 2 and category.lower() == "gifts":
        candidates.extend(_search_duckduckgo(query, limit=3))

    if not candidates:
        candidates.extend(_fallback_candidates(query, category))

    deduped: dict[str, ProductCandidate] = {}
    for candidate in candidates:
        key = re.sub(r"\W+", "", candidate.title.lower())[:80]
        if key and key not in deduped:
            deduped[key] = candidate
    return list(deduped.values())[:limit]


@tool
def product_discovery_tool(query: str, category: str = "gifts") -> list[dict[str, Any]]:
    """Find purchasable product candidates across retailer APIs and web search."""
    return [candidate.to_cart_item() for candidate in discover_products(query, category)]
