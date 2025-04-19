import os
import json
import logging
from typing import Any, Dict
from fastapi import FastAPI, HTTPException
import httpx
from dotenv import load_dotenv
from data_models import WeatherRequest, WeatherResponse
from selectolax.parser import HTMLParser
from functools import lru_cache
import time


# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Validate API key
if not API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY in environment variables.")

# Initialize FastAPI app
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Utility function to extract weather snippets from HTML
def extract_weather_snippets(html: str) -> str:
    tree = HTMLParser(html)
    snippets = []

    for node in tree.css("div"):
        text = node.text(strip=True)
        if any(keyword in text.lower() for keyword in ["temperature", "humidity", "air quality", "°", "feels like", "wind", "condition"]):
            snippets.append(text)

    return "\n".join(snippets[:10])  # return top relevant sections

# Utility function to fetch HTML from the web
async def fetch_weather_html(location: str) -> str:
    """Fetch weather data HTML from DuckDuckGo."""
    query = f"{location} weather today"
    url = f"https://html.duckduckgo.com/html/?t=h_&q={query}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            logger.error(f"Failed to fetch weather data. Status code: {response.status_code}")
            raise HTTPException(status_code=500, detail="Failed to fetch weather data.")
        return response.text

# Utility function to generate a prompt for the LLM
def construct_prompt(location: str, html_snippet: str) -> str:
    """Construct the user prompt for the LLM."""
    return f"""
    Given the HTML from a web search for weather in {location}, extract this info:

    - location
    - temperature (include unit)
    - humidity (%)
    - air_quality (e.g., Good, Moderate, Poor)
    - condition (e.g., Sunny, Rainy, Cloudy)

    Only respond with a valid JSON object.

    HTML snippet:

    ```html
    {html_snippet[:4000]}
    """

# Utility function to call OpenAI API
async def call_openai_api(prompt: str) -> Dict[str, Any]:
    """Call the OpenAI API with the given prompt."""
    import openai
    client = openai.OpenAI(api_key=API_KEY)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a weather data extractor."},
                {"role": "user", "content": f"""
            Extract the following details from the given HTML text:
            - location
            - temperature
            - humidity
            - air_quality
            - condition

            Text:
            {prompt}
            """}
            ],
            temperature=0,
            max_tokens=2000,
            response_format={"type": "json_object"}
        )
        # return json.loads(response.choices[0].message.content.strip())
        llm_reply = response.choices[0].message.content
        parsed_data = json.loads(llm_reply)
        
         # Extract usage data and convert it to a dictionary
        usage_data = response.usage if hasattr(response, 'usage') else {}  # Includes prompt_tokens, completion_tokens, total_tokens
        usage_dict = {
            "completion_tokens": usage_data.completion_tokens,
            "prompt_tokens": usage_data.prompt_tokens,
            "total_tokens": usage_data.total_tokens,
            "completion_tokens_details": vars(usage_data.completion_tokens_details),
            "prompt_tokens_details": vars(usage_data.prompt_tokens_details),
        } if usage_data else {}
        
        print(f"parsed_data in server: {parsed_data}")
        print(f"usage in server: {usage_dict}")
        
        # Return the parsed data along with usage information
        return {
            "location": parsed_data.get("location", "Unknown"),
            "temperature": parsed_data.get("temperature", "Unknown"),
            "humidity": parsed_data.get("humidity", "Unknown"),
            "air_quality": parsed_data.get("air_quality", "Unknown"),
            "condition": parsed_data.get("condition", "Unknown"),
            "usage": usage_dict
        }

    except Exception as e:
        logger.error(f"Error calling OpenAI API: {e}")
        raise HTTPException(status_code=500, detail="Failed to process weather data.")

@lru_cache(maxsize=100)
async def cached_weather_response(location: str) -> dict:
    # simulate a key lookup with internal logic
    print(f"Fetching fresh weather for: {location}")
    """
    Endpoint to get weather data for a given location.
    """
    try:
        # Step 1: Fetch HTML
        raw_html = await fetch_weather_html(location)

        # Step #2: Extract relevant snippets
        cleaned_text = extract_weather_snippets(raw_html)
        
        # Step 3: Construct prompt
        prompt = construct_prompt(location, cleaned_text)
        
        # Step 3: Call OpenAI API
        weather_data = await call_openai_api(prompt)

        # Step 4: Return response
        return weather_data
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

# Main endpoint
@app.post("/weather", response_model=WeatherResponse)
async def get_weather(request: WeatherRequest):
    data = await cached_weather_response(request.location)
    return WeatherResponse(**data)