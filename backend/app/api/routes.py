import logging
from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request

from app.agents.gift_planner_agent import GiftPlannerAgent
from app.services.db_service import db_service

api_bp = Blueprint("api_bp", __name__)
logger = logging.getLogger(__name__)
gift_planner = GiftPlannerAgent(db_service)


def extract_event_name(summary: str) -> str:
    if "_" in summary:
        return summary.split("_", 1)[0].lower()
    return summary.lower()


def extract_recipient_name(summary: str) -> str:
    if "_" in summary:
        return summary.split("_", 1)[1].replace("-", " ").strip()
    return summary


def _payload_for_preferences(data: dict, summary: str) -> dict:
    payload = {}
    for key in ("preferences", "budget", "birthday_date", "event_date", "relationship", "user_name"):
        if data.get(key) is not None:
            payload[key] = data.get(key)

    payload["event_name"] = extract_event_name(summary)
    payload["last_updated"] = datetime.utcnow().isoformat()
    return payload


@api_bp.route("/user-preferences", methods=["POST"])
def update_user_preferences():
    data = request.get_json(silent=True) or {}
    summary = data.get("summary")
    if not summary:
        return jsonify({"error": "The 'summary' field is required."}), 400

    try:
        update_payload = _payload_for_preferences(data, summary)
        db_service.create_or_update_event_user(summary, update_payload)
        return jsonify(
            {
                "status": "success",
                "message": f"Preferences for {summary} updated.",
                "event_name": update_payload["event_name"],
            }
        ), 200
    except Exception as exc:
        logger.exception("Error updating user preferences for %s", summary)
        return jsonify({"error": "Internal server error", "details": str(exc)}), 500


@api_bp.route("/trigger-event", methods=["POST"])
def trigger_event():
    data = request.get_json(silent=True) or {}
    summary = data.get("summary")
    if not summary:
        return jsonify({"error": "Missing 'summary' field."}), 400

    event_name = data.get("event_name") or extract_event_name(summary)

    try:
        user_data = db_service.get_user_by_summary(summary) or {}
        preferences = data.get("preferences") or user_data.get("preferences", ["books", "gadgets"])
        budget = data.get("budget") or user_data.get("budget", {"min": 100, "max": 500})
        user_name = (
            data.get("user_name")
            or user_data.get("user_name")
            or extract_recipient_name(summary)
        )

        profile_payload = {
            "user_name": user_name,
            "preferences": preferences,
            "budget": budget,
            "event_name": event_name,
            "birthday_date": data.get("birthday_date") or user_data.get("birthday_date"),
            "event_date": data.get("event_date") or user_data.get("event_date"),
            "relationship": data.get("relationship") or user_data.get("relationship"),
            "last_updated": datetime.utcnow().isoformat(),
        }
        db_service.create_or_update_event_user(summary, profile_payload)

        result = gift_planner.build_event_plan(
            summary=summary,
            event_type=event_name,
            person_name=user_name,
            preferences=preferences,
            budget=budget,
        )
        db_service.save_agent_run(summary, result)
        db_service.create_or_update_event_user(
            summary,
            {
                "last_agent_result": result,
                "last_agent_run_at": result["generated_at"],
                "notification": result["notification"],
            },
        )

        return jsonify(result), 200
    except Exception as exc:
        logger.exception("Error in /trigger-event for summary %s", summary)
        return jsonify({"error": "Internal server error", "details": str(exc)}), 500


@api_bp.route("/agent-runs/<path:summary>/latest", methods=["GET"])
def latest_agent_run(summary):
    try:
        run = db_service.get_latest_agent_run(summary)
        if not run:
            return jsonify({"error": "No agent run found."}), 404
        return jsonify(run), 200
    except Exception as exc:
        logger.exception("Error loading latest agent run for %s", summary)
        return jsonify({"error": "Internal server error", "details": str(exc)}), 500


@api_bp.route("/birthdays/due", methods=["GET"])
def due_birthdays():
    """Return recipients with birthdays/events in the next N days for notification UIs."""
    try:
        days = max(1, min(int(request.args.get("days", 7)), 365))
    except ValueError:
        return jsonify({"error": "'days' must be a number between 1 and 365."}), 400

    today = datetime.utcnow().date()
    end_date = today + timedelta(days=days)

    due = []
    for summary in db_service.list_all_summaries():
        user = db_service.get_user_by_summary(summary) or {}
        date_text = user.get("birthday_date") or user.get("event_date")
        if not date_text:
            continue
        try:
            parsed = datetime.fromisoformat(str(date_text).replace("Z", "+00:00")).date()
        except ValueError:
            continue

        try:
            anniversary = parsed.replace(year=today.year)
        except ValueError:
            anniversary = parsed.replace(year=today.year, day=28)
        if anniversary < today:
            try:
                anniversary = anniversary.replace(year=today.year + 1)
            except ValueError:
                anniversary = anniversary.replace(year=today.year + 1, day=28)

        if today <= anniversary <= end_date:
            due.append(
                {
                    "summary": summary,
                    "user_name": user.get("user_name") or extract_recipient_name(summary),
                    "event_name": user.get("event_name") or extract_event_name(summary),
                    "date": anniversary.isoformat(),
                    "notification": user.get("notification")
                    or f"{summary} has an upcoming celebration. Generate a gift plan.",
                }
            )

    return jsonify({"days": days, "events": due}), 200
