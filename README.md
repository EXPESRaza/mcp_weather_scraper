# MCP Weather Scraper

MCP Weather Scraper is a FastAPI-based application that fetches weather data for a given location by scraping HTML from DuckDuckGo and processing it using OpenAI's GPT model. The application provides a `/weather` endpoint to retrieve weather information in JSON format.

---

## Features

- **Weather Data Scraping**: Fetches weather-related HTML data from DuckDuckGo for a given location.
- **OpenAI Integration**: Uses OpenAI's GPT model to extract structured weather information from the HTML.
- **FastAPI Framework**: Provides a RESTful API endpoint for easy integration.
- **Error Handling**: Includes robust error handling for HTTP requests and API calls.
- **Environment Configuration**: Uses `.env` files to securely manage API keys.

---

## Requirements

- Python 3.9 or higher
- Dependencies listed in `requirements.txt`

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/mcp_weather_scraper.git
   cd mcp_weather_scraper
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a .env file in the root directory and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```

## Usage

### Running the Server

1. Start the FastAPI server:
   uvicorn server:app --reload

2. The server will be available at http://localhost:8000.

3. You can access the API documentation at:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Making a Request

#### Using curl command:

```bash
curl -X POST http://localhost:8000/weather -H "Content-Type: application/json" -d '{"location": "Seattle"}'
```

#### Using Client.py script:

You can use the provided client.py script to make a request to the /weather endpoint.

1. Ensure the server is running.
2. Run the client.py script:
   python [client.py](http://_vscodecontentref_/1)

   The script sends a POST request with the following payload:

   ```json
   {
     "location": "Seattle"
   }
   ```

   The server will respond with weather data in JSON format, such as:

   ```json
   {
     "location": "Seattle",
     "temperature": "15°C",
     "humidity": "80%",
     "air_quality": "Good",
     "condition": "Cloudy"
   }
   ```
