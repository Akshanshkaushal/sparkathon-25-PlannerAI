import logging
from typing import Any

from app.agents.product_tools import discover_products

logger = logging.getLogger(__name__)


def _max_budget(budget: Any) -> float:
    if isinstance(budget, dict):
        return float(budget.get("max") or budget.get("max_budget") or 500)
    try:
        return float(budget)
    except (TypeError, ValueError):
        return 500.0


def _query_from_item(item: Any) -> str:
    if isinstance(item, dict):
        return item.get("query") or item.get("name") or item.get("title") or str(item)
    return str(item)


def run_trend_ai(product_list: list, budget: Any, category: str) -> dict:
    """
    Backward-compatible product selection agent.

    The old version only asked the LLM to pick from a static list. This version uses
    live product discovery tools, filters by budget, and returns the same cart item
    shape the frontend already expects.
    """
    max_budget = _max_budget(budget)
    query = " ".join(_query_from_item(item) for item in product_list[:3]) or category
    candidates = discover_products(query, category)
    if not candidates:
        logger.warning("No product candidates found for %s", query)
        return {
            "source": "No Results",
            "title": f"No valid recommendation for {category}",
            "price": {"currentPrice": "0.00", "currency": "$"},
            "link": "",
            "reviewsCount": "N/A",
            "isBestSeller": False,
        }

    under_budget = [candidate for candidate in candidates if candidate.price <= max_budget]
    selected = sorted(
        under_budget or candidates,
        key=lambda candidate: (candidate.is_best_seller, candidate.price <= max_budget, -candidate.price),
        reverse=True,
    )[0]
    selected.rationale = "Selected by product discovery agent using budget fit and source quality."
    return selected.to_cart_item()


def create_trend_agent_executor():
    return lambda product_list, budget, category: run_trend_ai(product_list, budget, category)
