import requests
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# This is the key for the specific Walmart API you are using from RapidAPI
WALMART_API_KEY = os.environ.get('WALMART_API_KEY')
# The host will be something like 'walmart-data-unofficial.p.rapidapi.com'
WALMART_API_HOST = "walmart-data-unofficial.p.rapidapi.com" 

def search_walmart_product(query: str) -> list[dict]:
    """
    Searches for a product on Walmart using the RapidAPI and returns a list of
    structured product data. This function is designed to be used as a tool by an agent.
    """
    if not WALMART_API_KEY or not WALMART_API_HOST:
        logger.error("Walmart API Key or Host is not configured in environment variables.")
        return []

    url = f"https://{WALMART_API_HOST}/search"
    
    querystring = {"query": query}

    headers = {
        "x-rapidapi-key": WALMART_API_KEY,
        "x-rapidapi-host": WALMART_API_HOST
    }

    try:
        logger.info(f"Calling Walmart RapidAPI with query: '{query}'")
        response = requests.get(url, headers=headers, params=querystring, timeout=15)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        data = response.json()
        products = data.get("body", {}).get("products", [])

        if not products:
            logger.warning(f"No products found on Walmart for query: '{query}'")
            return []

        formatted_products = []
        for product in products[:3]: # Limit to top 3 results to keep it concise
            price_info = product.get("price", {})
            formatted_product = {
                "source": "Walmart API",
                "title": product.get("title"),
                "image": product.get("image"),
                "link": product.get("link"),
                "price": {
                    "currentPrice": price_info.get("currentPrice"),
                    "currency": price_info.get("currency", "$")
                },
                "reviewsCount": product.get("reviewsCount"),
                "isBestSeller": product.get("isBestSeller", False)
            }
            formatted_products.append(formatted_product)
        
        logger.info(f"Successfully formatted {len(formatted_products)} products from Walmart.")
        return formatted_products

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data from Walmart RapidAPI: {e}")
        return []
    except (KeyError, IndexError) as e:
        logger.error(f"Error parsing Walmart API response: {e}")
        return []