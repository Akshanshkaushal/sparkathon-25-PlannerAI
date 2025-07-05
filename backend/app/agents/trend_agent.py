import os
import json
import logging
from langchain_openai import AzureChatOpenAI
from langchain.agents import tool, create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from app.services.walmart_service import search_walmart_product

# Configure logging
logger = logging.getLogger(__name__)

# Define the search function as a LangChain tool
@tool
def walmart_product_search(query: str) -> str:
    """
    Use this tool to find specific products, their prices, and deals from Walmart.
    The input should be a precise product search query (e.g., 'Sony WH-1000XM5 headphones').
    It returns a list of products with their details in a JSON string format.
    """
    results = search_walmart_product(query)
    return json.dumps(results)

def create_trend_agent_executor():
    """
    Creates and returns a LangChain AgentExecutor.
    This agent is designed to find the best product deal for a given item and budget.
    It has access to a Walmart Product Search tool.
    """
    llm = AzureChatOpenAI(
        temperature=0, # We want deterministic and structured output
        azure_deployment=os.environ.get('AZURE_OPENAI_GPT_DEPLOYMENT_NAME'),
        api_version="2023-05-15"
    )

    tools = [walmart_product_search]

    # This prompt is the agent's "brain". It tells it how to think and what to do.
    prompt_template = """
    You are an expert shopping assistant. Your goal is to find the single best product deal for a user-specified item, staying within their budget.

    You have access to the following tools:
    {tools}

    **Your Task:**
    1.  You will be given an item to find and a budget.
    2.  First, ALWAYS use the `walmart_product_search` tool to find the item on Walmart.
    3.  Analyze the search results from the tool. Pick the single best option that fits the budget and has good value (consider price and reviews).
    4.  If the tool returns no results or nothing within budget, use your own general knowledge to suggest a suitable product.
        - If using your own knowledge, clearly state the source as 'OpenAI General Knowledge'.
        - Provide a realistic estimated price.
        - For the link,from flask import Blueprint, jsonify, request, current_app
from app.services.db_service import get_user_preferences, add_user_preference
from app.agents.goal_agent import get_goal_agent_chain
from app.agents.budget_agent import get_budget_agent_chain
from app.agents.trend_agent import create_trend_agent_executor # <-- Import the new agent creator
import json
import logging

api_bp = Blueprint('api_bp', __name__)
logger = logging.getLogger(__name__)

@api_bp.route('/trigger-event', methods=['POST'])
def trigger_event():
    data = request.json
    event_type = data.get('event_type')
    person_name = data.get('person_name')
    spending_tier = data.get('spending_tier', 'Mid-Range')

    try:
        # 1. Get user preferences
        preferences = get_user_preferences(person_name)

        # 2. Run Goal/Planner Agent
        goal_chain = get_goal_agent_chain()
        plan_result = goal_chain.invoke({"event_type": event_type, "person_name": person_name, "user_preferences": str(preferences)})
        plan_json = json.loads(plan_result['text'])
        logger.info(f"Planner Agent generated plan: {plan_json}")

        # 3. Run Budget Agent
        budget_chain = get_budget_agent_chain()
        budget_result = budget_chain.invoke({"spending_tier": spending_tier, "event_plan_json": json.dumps(plan_json)})
        budget_json = json.loads(budget_result['text'])
        logger.info(f"Budget Agent generated budget: {budget_json}")

        # 4. Initialize the Trend Agent Executor
        trend_agent_executor = create_trend_agent_executor()

        # 5. Sequentially find products for each item using the Trend Agent
        cart_items = {"gifts": [], "decorations": [], "cake": []}
        
        # Combine all items into a single list with their categories and budgets
        items_to_find = []
        for gift in plan_json.get('gift_suggestions', []):
            items_to_find.append({"category": "gifts", "item": gift['name'], "budget": budget_json.get('gift_suggestions', {}).get('max_budget')})
        
        for deco in plan_json.get('decoration_items', []):
             items_to_find.append({"category": "decorations", "item": deco, "budget": budget_json.get('decoration_items', {}).get('max_budget')})
        
        # For each item, invoke the trend agent to find the best product
        for item_info in items_to_find:
            category = item_info['category']
            item_description = item_info['item']
            item_budget = f"up to ${item_info['budget']}"

            logger.info(f"Invoking Trend Agent for: '{item_description}' with budget: '{item_budget}'")
            
            # The agent will now perform the search and decision-making
            agent_response = trend_agent_executor.invoke({
                "item_description": item_description,
                "budget": item_budget
            })
            
            # The final answer from the agent should be a JSON string
            product_json_string = agent_response['output']
            logger.info(f"Trend Agent found: {product_json_string}")
            
            try:
                # Safely parse the JSON output from the agent
                product_details = json.loads(product_json_string)
                cart_items[category].append(product_details)
            except json.JSONDecodeError:
                logger.error(f"Failed to parse JSON response from Trend Agent: {product_json_string}")
                # Append a placeholder error object to the cart
                cart_items[category].append({"source": "Error", "title": f"Could not find '{item_description}'", "price": {"currentPrice": "N/A"}})


        return jsonify({
            "plan": plan_json,
            "budget": budget_json,
            "cart": cart_items
        })

    except Exception as e:
        logger.exception("An unexpected error occurred in the /trigger-event endpoint.")
        return jsonify({"error": "An internal server error occurred.", "details": str(e)}), 500


@api_bp.route('/user-preferences', methods=['POST'])
def set_user_preferences():
    # This route remains the same
    data = request.json
    user_name = data.get('user_name')
    preferences = data.get('preferences')
    add_user_preference(user_name, preferences)
    return jsonify({"message": f"Preferences for {user_name} updated."}), 201 provide a generic Google search link for the product.
        - You must invent a plausible image URL for the product, for example: `https://via.placeholder.com/150.png?text=Product+Name`

    **Final Output Format:**
    You MUST respond with a single, clean JSON object representing the best product you found. Do not include any other text or explanation outside of the JSON object.

    The JSON object must have the following structure:
    {{
      "source": "Walmart API" or "OpenAI General Knowledge",
      "title": "Product Title",
      "image": "URL_to_image",
      "link": "URL_to_product_or_search_page",
      "price": {{
        "currentPrice": "price as a string, e.g., 79.00",
        "currency": "$"
      }},
      "reviewsCount": "number_of_reviews" or "N/A",
      "isBestSeller": true or false
    }}

    **Let's begin!**

    **Item to Find:** {item_description}
    **Budget:** {budget}

    **Thought Process and Action:**
    {agent_scratchpad}
    """

    prompt = PromptTemplate.from_template(prompt_template)
    
    agent = create_react_agent(llm, tools, prompt)
    
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True, # Set to True for debugging to see the agent's thoughts
        handle_parsing_errors=True # Gracefully handle if the LLM messes up formatting
    )

    return agent_executor