from __future__ import annotations

import json
import logging
import math
from datetime import datetime
from typing import Any

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from app.agents.json_utils import parse_json
from app.agents.llm import get_chat_model, is_llm_configured
from app.agents.memory import MongoRecipientMemory, summarize_memory
from app.agents.product_tools import ProductCandidate, discover_products

logger = logging.getLogger(__name__)


DEFAULT_BUDGET = {"min": 100, "max": 500}
CART_CATEGORIES = ("gifts", "decorations", "cake")


def _normalize_budget(budget: Any) -> dict[str, float]:
    if isinstance(budget, dict):
        min_budget = float(budget.get("min") or budget.get("min_budget") or DEFAULT_BUDGET["min"])
        max_budget = float(budget.get("max") or budget.get("max_budget") or DEFAULT_BUDGET["max"])
    else:
        min_budget = DEFAULT_BUDGET["min"]
        max_budget = DEFAULT_BUDGET["max"]

    if min_budget < 0:
        min_budget = 0
    if max_budget < min_budget:
        max_budget = min_budget
    return {"min": min_budget, "max": max_budget}


def _normalize_preferences(preferences: Any) -> list[str]:
    if isinstance(preferences, str):
        return [item.strip() for item in preferences.split(",") if item.strip()]
    if isinstance(preferences, list):
        return [str(item).strip() for item in preferences if str(item).strip()]
    return ["books", "gadgets"]


def _category_budget(total_budget: dict[str, float]) -> dict[str, dict[str, float]]:
    min_budget = total_budget["min"]
    max_budget = total_budget["max"]
    return {
        "gifts": {
            "min_budget": round(min_budget * 0.55, 2),
            "max_budget": round(max_budget * 0.65, 2),
        },
        "decorations": {
            "min_budget": round(min_budget * 0.20, 2),
            "max_budget": round(max_budget * 0.20, 2),
        },
        "cake": {
            "min_budget": round(min_budget * 0.25, 2),
            "max_budget": round(max_budget * 0.15, 2),
        },
    }


def _fallback_plan(
    event_type: str,
    person_name: str,
    preferences: list[str],
    budget: dict[str, float],
) -> dict[str, Any]:
    primary = preferences[0] if preferences else "personal interests"
    secondary = preferences[1] if len(preferences) > 1 else "daily usefulness"
    max_gift_price = round(budget["max"] * 0.65, 2)
    gift_queries = [
        f"best {primary} gift under {int(max_gift_price)}",
        f"personalized {primary} gift",
        f"{secondary} useful gift",
    ]

    return {
        "recipient_profile": {
            "name": person_name,
            "occasion": event_type,
            "preferences": preferences,
            "budget": budget,
            "known_facts": [],
            "avoid": [],
        },
        "gift_strategy": [
            {
                "name": f"{primary.title()} premium pick",
                "query": gift_queries[0],
                "category": "gifts",
                "why": f"Matches {person_name}'s stated interest in {primary}.",
                "target_price": max_gift_price,
            },
            {
                "name": f"Personalized {primary}",
                "query": gift_queries[1],
                "category": "gifts",
                "why": "Adds a personal touch while staying preference-led.",
                "target_price": round(max_gift_price * 0.7, 2),
            },
            {
                "name": f"{secondary.title()} everyday upgrade",
                "query": gift_queries[2],
                "category": "gifts",
                "why": "Balances novelty with practical use.",
                "target_price": round(max_gift_price * 0.55, 2),
            },
        ],
        "decoration_theme": f"{primary.title()} Celebration",
        "decoration_items": [
            f"{primary.title()} themed banner",
            "Warm string lights",
            "Photo memory wall",
            "Coordinated balloon kit",
            "Personalized table centerpiece",
        ],
        "cake_suggestion": {
            "type": f"{person_name}'s favorite flavor celebration cake",
            "size": "1.5 kg or 10-12 serving cake",
            "query": f"{event_type} cake order",
        },
        "notification": f"{event_type.title()} reminder for {person_name}: curated gifts are ready within budget.",
        "agent_reasoning_summary": "Fallback planner used deterministic preference and budget rules.",
    }


def _planning_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are PlannerAI's lead gift-planning agent.
Design a purchasable birthday or event plan, not a generic party essay.
Use remembered context when useful, obey the user's max budget, avoid unsafe/age-inappropriate gifts, and produce search-ready shopping queries.

Return STRICT JSON with this schema:
{{
  "recipient_profile": {{
    "name": string,
    "occasion": string,
    "preferences": [string],
    "budget": {{"min": number, "max": number}},
    "known_facts": [string],
    "avoid": [string]
  }},
  "gift_strategy": [
    {{"name": string, "query": string, "category": "gifts", "why": string, "target_price": number}}
  ],
  "decoration_theme": string,
  "decoration_items": [string],
  "cake_suggestion": {{"type": string, "size": string, "query": string}},
  "notification": string,
  "agent_reasoning_summary": string
}}
Rules:
- Make 3 to 5 gift_strategy entries.
- Queries must be concrete enough for shopping search.
- Do not invent live prices or product links.
- Keep the total plan realistic for the budget.""",
            ),
            MessagesPlaceholder(variable_name="history"),
            (
                "human",
                """Create a plan.
Event type: {event_type}
Recipient: {person_name}
Preferences: {preferences}
Budget: {budget}
Stored profile memory: {memory_summary}""",
            ),
        ]
    )


def _ranking_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a product ranking agent.
Choose the best purchasable item from candidates for the recipient.
Prefer items inside budget, with a real link, clear title, stronger preference fit, and social proof.
Return STRICT JSON:
{{
  "selected_title": string,
  "rationale": string,
  "score": number,
  "budget_fit": "under_budget" | "near_budget" | "over_budget" | "price_unverified"
}}""",
            ),
            (
                "human",
                """Recipient profile: {profile}
Category: {category}
Max category budget: {max_budget}
Gift intent: {intent}
Candidates: {candidates}""",
            ),
        ]
    )


class GiftPlannerAgent:
    """Coordinates planning, memory, product search, ranking, and cart assembly."""

    def __init__(self, db_service: Any):
        self.db_service = db_service

    def _memory_for(self, summary: str) -> MongoRecipientMemory:
        return MongoRecipientMemory(self.db_service, summary)

    def _invoke_planner(
        self,
        summary: str,
        event_type: str,
        person_name: str,
        preferences: list[str],
        budget: dict[str, float],
    ) -> dict[str, Any]:
        memory = self._memory_for(summary)
        fallback = _fallback_plan(event_type, person_name, preferences, budget)

        if not is_llm_configured():
            logger.info("Azure OpenAI is not configured; using deterministic planner fallback.")
            return fallback

        try:
            chain = _planning_prompt() | get_chat_model(temperature=0.3)
            response = chain.invoke(
                {
                    "event_type": event_type,
                    "person_name": person_name,
                    "preferences": json.dumps(preferences),
                    "budget": json.dumps(budget),
                    "memory_summary": summarize_memory(memory.messages),
                    "history": memory.messages,
                },
            )
            return parse_json(response.content, fallback, context="planner agent")
        except Exception:
            logger.exception("Planner agent failed; using deterministic fallback.")
            return fallback

    def _rank_candidate(
        self,
        profile: dict[str, Any],
        category: str,
        max_budget: float,
        intent: dict[str, Any],
        candidates: list[ProductCandidate],
    ) -> tuple[ProductCandidate | None, list[dict[str, Any]], dict[str, Any]]:
        if not candidates:
            return None, [], {"rationale": "No candidates discovered.", "score": 0}

        fallback_selected = sorted(
            candidates,
            key=lambda item: (
                item.price <= max_budget if item.price else False,
                item.is_best_seller,
                -abs((item.price or max_budget) - min(max_budget, item.price or max_budget)),
            ),
            reverse=True,
        )[0]
        fallback_rank = {
            "selected_title": fallback_selected.title,
            "rationale": "Selected by budget fit, availability, and preference-query match.",
            "score": 75,
            "budget_fit": "under_budget" if fallback_selected.price <= max_budget else "over_budget",
        }

        if not is_llm_configured():
            selected = fallback_selected
            rank = fallback_rank
        else:
            try:
                response = (_ranking_prompt() | get_chat_model(temperature=0)).invoke(
                    {
                        "profile": json.dumps(profile),
                        "category": category,
                        "max_budget": max_budget,
                        "intent": json.dumps(intent),
                        "candidates": json.dumps([candidate.to_cart_item() for candidate in candidates]),
                    }
                )
                rank = parse_json(response.content, fallback_rank, context="ranking agent")
                selected_title = str(rank.get("selected_title", "")).lower()
                selected = next(
                    (candidate for candidate in candidates if candidate.title.lower() == selected_title),
                    fallback_selected,
                )
            except Exception:
                logger.exception("Ranking agent failed; using heuristic rank.")
                rank = fallback_rank
                selected = fallback_selected

        alternatives = [
            candidate.to_cart_item()
            for candidate in candidates
            if candidate.title != selected.title
        ][:3]
        selected.rationale = rank.get("rationale", selected.rationale)
        return selected, alternatives, rank

    def _cart_for_category(
        self,
        profile: dict[str, Any],
        category: str,
        max_budget: float,
        intents: list[dict[str, Any]],
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
        cart: list[dict[str, Any]] = []
        alternatives: list[dict[str, Any]] = []
        trace: list[dict[str, Any]] = []

        for intent in intents:
            query = intent.get("query") or intent.get("name") or category
            candidates = discover_products(query, category)
            selected, alternate_items, rank = self._rank_candidate(
                profile,
                category,
                max_budget,
                intent,
                candidates,
            )
            trace.append(
                {
                    "agent": "ProductDiscoveryAgent+RankingAgent",
                    "category": category,
                    "query": query,
                    "candidate_count": len(candidates),
                    "rank": rank,
                }
            )
            if selected:
                cart.append(selected.to_cart_item())
            alternatives.extend(alternate_items)

            break

        return cart, alternatives, trace

    def build_event_plan(
        self,
        summary: str,
        event_type: str,
        person_name: str,
        preferences: Any,
        budget: Any,
    ) -> dict[str, Any]:
        normalized_preferences = _normalize_preferences(preferences)
        normalized_budget = _normalize_budget(budget)
        category_budgets = _category_budget(normalized_budget)

        plan = self._invoke_planner(
            summary,
            event_type,
            person_name,
            normalized_preferences,
            normalized_budget,
        )
        profile = plan.get("recipient_profile") or {}
        gift_strategy = plan.get("gift_strategy") or []
        if not gift_strategy:
            gift_strategy = _fallback_plan(event_type, person_name, normalized_preferences, normalized_budget)["gift_strategy"]

        cart = {category: [] for category in CART_CATEGORIES}
        alternatives = {category: [] for category in CART_CATEGORIES}
        agent_trace = [
            {
                "agent": "ProfileMemoryAgent",
                "summary": "Loaded recipient preferences and recent conversation from Mongo-backed LangChain chat history.",
            },
            {
                "agent": "OccasionPlannerAgent",
                "summary": plan.get("agent_reasoning_summary", "Created gift strategy and party plan."),
            },
        ]

        gift_cart, gift_alternatives, trace = self._cart_for_category(
            profile,
            "gifts",
            category_budgets["gifts"]["max_budget"],
            gift_strategy,
        )
        cart["gifts"] = gift_cart
        alternatives["gifts"] = gift_alternatives
        agent_trace.extend(trace)

        decoration_query = f"{plan.get('decoration_theme', event_type)} party decorations"
        decor_intents = [{"name": "Decoration kit", "query": decoration_query, "category": "decorations"}]
        decor_cart, decor_alternatives, trace = self._cart_for_category(
            profile,
            "decorations",
            category_budgets["decorations"]["max_budget"],
            decor_intents,
        )
        cart["decorations"] = decor_cart
        alternatives["decorations"] = decor_alternatives
        agent_trace.extend(trace)

        cake_suggestion = plan.get("cake_suggestion") or {}
        cake_query = cake_suggestion.get("query") or cake_suggestion.get("type") or f"{event_type} cake"
        cake_cart, cake_alternatives, trace = self._cart_for_category(
            profile,
            "cake",
            category_budgets["cake"]["max_budget"],
            [{"name": cake_suggestion.get("type", "Cake"), "query": cake_query, "category": "cake"}],
        )
        cart["cake"] = cake_cart
        alternatives["cake"] = cake_alternatives
        agent_trace.extend(trace)

        specific_gifts = [
            {
                "name": item.get("name") or item.get("query") or "Gift idea",
                "description": item.get("why", "Matches the recipient profile."),
            }
            for item in gift_strategy[:3]
        ]
        inspired_gifts = [
            {
                "name": item.get("name") or item.get("query") or "Inspired gift idea",
                "description": item.get("why", "Inspired by the recipient's adjacent interests."),
            }
            for item in gift_strategy[3:5]
        ]

        frontend_plan = {
            "recipient_profile": profile,
            "gift_suggestions": {
                "specific_gifts": specific_gifts,
                "inspired_by_gifts": inspired_gifts,
            },
            "gift_strategy": gift_strategy,
            "decoration_theme": plan.get("decoration_theme", f"{event_type.title()} Celebration"),
            "decoration_items": plan.get("decoration_items", []),
            "cake_suggestion": cake_suggestion,
        }

        total_estimate = math.fsum(
            float(item.get("price", {}).get("currentPrice") or 0)
            for items in cart.values()
            for item in items
        )
        result = {
            "plan": frontend_plan,
            "budget": category_budgets,
            "cart": cart,
            "alternatives": alternatives,
            "notification": plan.get(
                "notification",
                f"{event_type.title()} reminder for {person_name}: curated gifts are ready.",
            ),
            "checkout": {
                "status": "ready_for_review",
                "estimated_total": round(total_estimate, 2),
                "currency": "$",
                "requires_user_confirmation": True,
            },
            "agent_trace": agent_trace,
            "generated_at": datetime.utcnow().isoformat(),
        }

        memory = self._memory_for(summary)
        memory.remember_turn(
            f"Preferences={normalized_preferences}; budget={normalized_budget}; event={event_type}",
            json.dumps(
                {
                    "notification": result["notification"],
                    "cart_titles": [
                        item.get("title")
                        for items in cart.values()
                        for item in items
                    ],
                    "estimated_total": result["checkout"]["estimated_total"],
                }
            ),
        )
        return result
