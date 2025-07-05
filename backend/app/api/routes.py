from flask import Blueprint, jsonify, request
from app.services.db_service import (
    get_user_preferences_by_email,
    get_user_spending_tier_by_email,
    create_or_update_user
)
from app.agents.goal_agent import get_goal_agent_chain
from app.agents.budget_agent import get_budget_agent_chain
from app.agents.trend_agent import create_trend_agent_executor
import json
import logging

api_bp = Blueprint('api_bp', __name__)
logger = logging.getLogger(__name__)

@api_bp.route('/trigger-event', methods=['POST'])
def trigger_event():
    data = request.json
    event_type = data.get('event_type')
    email = data.get('email')
    user_name = data.get('user_name')

    if not email:
        return jsonify({"error": "Email is required as unique user identifier."}), 400

    try:
        # 1. Resolve preferences
        preferences = data.get('preferences')
        if not preferences:
            preferences = get_user_preferences_by_email(email)
            if not preferences:
                preferences = ["books", "electronics"]
                logger.info(f"No preferences found for {email}, using defaults: {preferences}")

        # 2. Resolve spending tier
        spending_tier = data.get('spending_tier')
        if not spending_tier:
            spending_tier = get_user_spending_tier_by_email(email)
            if not spending_tier:
                spending_tier = "Mid-Range"
                logger.info(f"No spending tier found for {email}, using default: {spending_tier}")

        # 3. Save/update user in DB
        create_or_update_user(
            user_name=user_name or "Unknown",
            email=email,
            preferences=preferences,
            spending_tier=spending_tier
        )

        # 4. Run Planner Agent
        goal_chain = get_goal_agent_chain()
        plan_result = goal_chain.invoke({
            "event_type": event_type,
            "person_name": user_name or email,
            "user_preferences": str(preferences)
        })
        plan_json = json.loads(plan_result['text'])
        logger.info(f"Planner Agent returned: {plan_json}")

        # 5. Run Budget Agent
        budget_chain = get_budget_agent_chain()
        budget_result = budget_chain.invoke({
            "spending_tier": spending_tier,
            "event_plan_json": json.dumps(plan_json)
        })
        budget_json = json.loads(budget_result['text'])
        logger.info(f"Budget Agent returned: {budget_json}")

        # 6. Initialize Trend Agent
        trend_agent_executor = create_trend_agent_executor()

        # 7. Build cart dynamically
        cart_items = {}
        items_to_find = []

        for category, items in plan_json.items():
            if not isinstance(items, list):
                continue  # skip non-list fields
            cart_items[category] = []
            budget_for_category = budget_json.get(category, {}).get('max_budget')
            for item in items:
                item_name = item.get('name') if isinstance(item, dict) else item
                items_to_find.append({
                    "category": category,
                    "item": item_name,
                    "budget": budget_for_category
                })

        # 8. Find products for each item using Trend Agent
        for item_info in items_to_find:
            category = item_info['category']
            item_description = item_info['item']
            item_budget = f"up to ${item_info['budget']}" if item_info['budget'] else "any budget"

            logger.info(f"Invoking Trend Agent for '{item_description}' in '{category}' with '{item_budget}'")

            agent_response = trend_agent_executor.invoke({
                "item_description": item_description,
                "budget": item_budget
            })

            product_json_string = agent_response.get('output', '{}')
            try:
                product_details = json.loads(product_json_string)
                cart_items[category].append(product_details)
            except json.JSONDecodeError:
                logger.error(f"Failed to parse Trend Agent JSON: {product_json_string}")
                cart_items[category].append({
                    "source": "Error",
                    "title": f"Could not find '{item_description}'",
                    "price": {"currentPrice": "N/A"}
                })

        return jsonify({
            "plan": plan_json,
            "budget": budget_json,
            "cart": cart_items
        })

    except Exception as e:
        logger.exception("Unexpected error in /trigger-event.")
        return jsonify({"error": "Internal server error.", "details": str(e)}), 500


@api_bp.route('/user-preferences', methods=['POST'])
def set_user_preferences():
    data = request.json
    email = data.get('email')
    user_name = data.get('user_name')
    preferences = data.get('preferences')
    spending_tier = data.get('spending_tier')

    if not email:
        return jsonify({"error": "Email is required as unique user identifier."}), 400

    create_or_update_user(
        user_name=user_name or "Unknown",
        email=email,
        preferences=preferences,
        spending_tier=spending_tier
    )

    return jsonify({"message": f"Preferences and spending tier for {email} updated."}), 201
