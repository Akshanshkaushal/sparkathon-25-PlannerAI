import json
import logging
from typing import Any

from langchain_core.prompts import ChatPromptTemplate

from app.agents.gift_planner_agent import _fallback_plan, _normalize_budget, _normalize_preferences
from app.agents.json_utils import parse_json
from app.agents.llm import get_chat_model

logger = logging.getLogger(__name__)


class GoalAgentChain:
    """Backward-compatible chain wrapper for older route imports."""

    def __init__(self):
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are the occasion planning agent for PlannerAI.
Create a concise, purchasable event plan from preferences and return strict JSON:
{{
  "gift_suggestions": {{
    "specific_gifts": [{{"name": string, "description": string}}],
    "inspired_by_gifts": [{{"name": string, "description": string}}]
  }},
  "decoration_theme": string,
  "decoration_items": [string],
  "cake_suggestion": {{"type": string, "size": string, "query": string}}
}}""",
                ),
                (
                    "human",
                    "Event: {event_type}\nRecipient: {person_name}\nPreferences: {user_preferences}",
                ),
            ]
        )

    def invoke(self, inputs: dict[str, Any]) -> dict[str, str]:
        event_type = inputs.get("event_type", "birthday")
        person_name = inputs.get("person_name", "recipient")
        preferences = _normalize_preferences(inputs.get("user_preferences", []))
        fallback = _fallback_plan(event_type, person_name, preferences, _normalize_budget({}))
        fallback_output = {
            "gift_suggestions": {
                "specific_gifts": [
                    {"name": item["name"], "description": item["why"]}
                    for item in fallback["gift_strategy"][:3]
                ],
                "inspired_by_gifts": [
                    {"name": item["name"], "description": item["why"]}
                    for item in fallback["gift_strategy"][3:5]
                ],
            },
            "decoration_theme": fallback["decoration_theme"],
            "decoration_items": fallback["decoration_items"],
            "cake_suggestion": fallback["cake_suggestion"],
        }

        try:
            response = (self.prompt | get_chat_model(temperature=0.3)).invoke(inputs)
            parsed = parse_json(response.content, fallback_output, context="goal agent")
            return {"text": json.dumps(parsed)}
        except Exception:
            logger.exception("Goal agent failed; using fallback.")
            return {"text": json.dumps(fallback_output)}


def get_goal_agent_chain():
    return GoalAgentChain()
