from flask import Blueprint, jsonify, request
from app.agents.goal_agent import get_goal_agent_chain
from app.agents.budget_agent import get_budget_agent_chain
from app.agents.trend_agent import run_trend_ai  # Changed from create_trend_agent_executor
from app.services.db_service import db_service
import json
import logging
import re
from datetime import datetime

api_bp = Blueprint('api_bp', __name__)
logger = logging.getLogger(__name__)


def extract_event_name(summary: str) -> str:
    if "_" in summary:
        return summary.split("_")[0].lower()
    return summary.lower()


def extract_json_from_text(raw_text: str) -> str:
    """
    Extract JSON from text that might be wrapped in markdown fences like ```json ... ```
    """
    # remove code block fences
    code_fence_pattern = r"```(?:json)?\s*(.*?)```"
    match = re.search(code_fence_pattern, raw_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return raw_text.strip()


def try_parse_json(raw_text, context=""):
    """
    Safely attempts to parse JSON string. Cleans fenced code blocks first.
    """
    clean_text = extract_json_from_text(raw_text)
    try:
        return json.loads(clean_text)
    except json.JSONDecodeError:
        logger.error(f"❌ Failed to parse JSON from {context}. Raw cleaned text was:\n{clean_text}")
        raise


@api_bp.route('/user-preferences', methods=['POST'])
def update_user_preferences():
    data = request.json
    summary = data.get('summary')
    preferences = data.get('preferences')
    budget = data.get('budget')

    if not summary:
        return jsonify({"error": "The 'summary' field is required."}), 400

    try:
        update_data = {}
        if preferences is not None:
            update_data['preferences'] = preferences
        if budget is not None:
            update_data['budget'] = budget

        event_name = extract_event_name(summary)
        update_data['event_name'] = event_name
        update_data['last_updated'] = datetime.utcnow().isoformat()

        db_service.create_or_update_event_user(summary, update_data)

        return jsonify({
            "status": "success",
            "message": f"Preferences for {summary} updated.",
            "event_name": event_name
        }), 200

    except Exception as e:
        logger.exception(f"Error updating user preferences for {summary}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@api_bp.route('/trigger-event', methods=['POST'])
def trigger_event():
    data = request.json
    summary = data.get('summary')
    if not summary:
        return jsonify({"error": "Missing 'summary' field."}), 400

    event_name = extract_event_name(summary)

    try:
        # -------------------- User data --------------------
        user_data = db_service.get_user_by_summary(summary) or {}
        preferences = data.get('preferences') or user_data.get('preferences', ["books", "gadgets"])
        budget = data.get('budget') or user_data.get('budget', {"min": 100, "max": 500})
        user_name = data.get('user_name') or user_data.get('user_name', summary.split('@')[0])

        update_payload = {
            "user_name": user_name,
            "preferences": preferences,
            "budget": budget,
            "event_name": event_name,
            "last_updated": datetime.utcnow().isoformat()
        }
        db_service.create_or_update_event_user(summary, update_payload)

        # -------------------- Agents --------------------
        goal_chain = get_goal_agent_chain()
        plan_result = goal_chain.invoke({
            "event_type": event_name,
            "person_name": user_name,
            "user_preferences": str(preferences)
        })

        logger.info(f"📝 Planner agent output:\n{plan_result}")
        plan_json = try_parse_json(plan_result.get('text', ''), context="Planner Agent")

        budget_chain = get_budget_agent_chain()
        budget_result = budget_chain.invoke({
            "spending_tier": budget,
            "event_plan_json": json.dumps(plan_json)
        })

        logger.info(f"💵 Budget agent output:\n{budget_result}")
        budget_json = try_parse_json(budget_result.get('text', ''), context="Budget Agent")

        # -------------------- Trend shopping --------------------
        cart_items = {}

        for category, items in plan_json.items():
            if not isinstance(items, list):
                continue
            cart_items[category] = []

            category_budget = budget_json.get(category, {}).get('max_budget', budget['max'])
            
            # Run our trend AI to pick best from list
            best_product = run_trend_ai(items, category_budget, category)
            cart_items[category].append(best_product)

        return jsonify({
            "plan": plan_json,
            "budget": budget_json,
            "cart": cart_items
        }), 200

    except Exception as e:
        logger.exception("Error in /trigger-event")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
