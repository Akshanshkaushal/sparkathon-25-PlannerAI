from flask import Blueprint, jsonify, request
from app.agents.goal_agent import get_goal_agent_chain
from app.agents.budget_agent import get_budget_agent_chain
from app.agents.trend_agent import create_trend_agent_executor
from app.services.db_service import db_service
import json
import logging
from datetime import datetime

api_bp = Blueprint('api_bp', __name__)
logger = logging.getLogger(__name__)

@api_bp.route('/user-preferences', methods=['POST'])
def update_user_preferences():
    """
    Update a user's preferences and budget using 'summary' as unique identifier.
    """
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

        if not update_data:
            return jsonify({"error": "No data to update (preferences or budget)."}), 400

        db_service.create_or_update_event_user(summary, update_data)

        return jsonify({"status": "success", "message": f"Preferences for {summary} updated."}), 200

    except Exception as e:
        logger.exception(f"Error updating user preferences for {summary}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@api_bp.route('/trigger-event', methods=['POST'])
def trigger_event():
    """
    Triggered by a calendar event. Uses 'summary' as unique identifier.
    """
    data = request.json
    summary = data.get('summary')
    if not summary:
        return jsonify({"error": "Missing 'summary' field."}), 400

    event_name = data.get('event_name', 'General')

    try:
        # Fetch existing user data by summary
        user_data = db_service.get_user_by_summary(summary) or {}

        preferences = data.get('preferences') or user_data.get('preferences', ["books", "electronics"])
        budget = data.get('budget') or user_data.get('budget', "Mid-Range")
        user_name = data.get('user_name') or user_data.get('user_name', summary.split('@')[0])

        update_payload = {
            "user_name": user_name,
            "preferences": preferences,
            "budget": budget,
            "event_name": event_name,
            "last_updated": datetime.utcnow().isoformat()
        }

        db_service.create_or_update_event_user(summary, update_payload)

        # --- Agent pipeline ---

        goal_chain = get_goal_agent_chain()
        plan_result = goal_chain.invoke({
            "event_type": event_name,
            "person_name": user_name,
            "user_preferences": str(preferences)
        })
        plan_json = json.loads(plan_result['text'])
        logger.info(f"🧠 Planner Agent returned: {plan_json}")

        budget_chain = get_budget_agent_chain()
        budget_result = budget_chain.invoke({
            "spending_tier": budget,
            "event_plan_json": json.dumps(plan_json)
        })
        budget_json = json.loads(budget_result['text'])
        logger.info(f"💰 Budget Agent returned: {budget_json}")

        trend_agent_executor = create_trend_agent_executor()
        cart_items = {}
        items_to_find = []

        for category, items in plan_json.items():
            if not isinstance(items, list):
                continue
            cart_items[category] = []
            category_budget = budget_json.get(category, {}).get('max_budget')

            for item in items:
                item_name = item.get('name') if isinstance(item, dict) else item
                items_to_find.append({
                    "category": category,
                    "item": item_name,
                    "budget": category_budget
                })

        for item_info in items_to_find:
            category = item_info['category']
            item_description = item_info['item']
            item_budget = f"up to ${item_info['budget']}" if item_info['budget'] else "any budget"
            logger.info(f"🛒 Looking for '{item_description}' in '{category}' with {item_budget}")
            agent_response = trend_agent_executor.invoke({
                "item_description": item_description,
                "budget": item_budget
            })
            product_json_string = agent_response.get('output', '{}')
            try:
                product_details = json.loads(product_json_string)
                cart_items[category].append(product_details)
            except json.JSONDecodeError:
                logger.error(f"❌ Failed to parse product JSON: {product_json_string}")
                cart_items[category].append({
                    "source": "Error",
                    "title": f"Could not find '{item_description}'"
                })

        return jsonify({
            "plan": plan_json,
            "budget": budget_json,
            "cart": cart_items
        }), 200

    except Exception as e:
        logger.exception("Error in /trigger-event")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
