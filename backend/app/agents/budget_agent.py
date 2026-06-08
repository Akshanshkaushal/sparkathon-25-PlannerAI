import json
from typing import Any

from app.agents.gift_planner_agent import _category_budget, _normalize_budget


class BudgetAgentChain:
    """Deterministic budget allocator with the old LLMChain-style interface."""

    def invoke(self, inputs: dict[str, Any]) -> dict[str, str]:
        budget = _normalize_budget(inputs.get("spending_tier"))
        return {"text": json.dumps(_category_budget(budget))}


def get_budget_agent_chain():
    return BudgetAgentChain()
