# 🌦️ MCP Weather Scraper

A minimal working example of integrating an LLM (via Ollama or OpenAI) with an [MCP (Model Context Protocol)](https://github.com/ai-dot-ai/model-context-protocol) server to fetch and extract real-time weather data from the web.

---

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/github/license/EXPESRaza/mcp_weather_scraper)](LICENSE)
[![Issues](https://img.shields.io/github/issues/EXPESRaza/mcp_weather_scraper)](https://github.com/EXPESRaza/mcp_weather_scraper/issues)

---

## 🚀 Features

- 🌍 Query weather data via natural language prompts
- 📡 Scrape real-time results from the open web
- 🧠 Extract structured weather info using an LLM
- ⚡ Fast in-memory caching for repeated queries
- 🧹 HTML cleanup with `selectolax` for more focused extraction

---

## Requirements

- Python 3.9 or higher
- Dependencies listed in `requirements.txt`

---

## 🛠️ Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/mcp_weather_scraper.git
   cd mcp_weather_scraper
   ```
2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set environment variables**
   Create a .env file in the root directory and add your OpenAI API key
   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```

5. **Running the Server**
   ```bash
   uvicorn server:app --reload
   ```
   The server will be available at http://localhost:8000.

6. You can access the API documentation at:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

7. **Making a Request**
   ```bash
   python client.py
   ```
   OR
   ```bash
   curl -X POST http://localhost:8000/weather -H "Content-Type: application/json" -d '{"location": "Seattle"}'
   ```
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

## 📦 Folder Structure
```bash
.
├── server.py          # MCP-compatible tool server
├── client.py          # MCP client that interacts with model + tools
├── data_models.py     # Pydantic schemas for request/response
├── utils.py           # HTML cleaning, scraping, etc.
├── requirements.txt
└── .env
```

## 📄 License
```yaml
This project is licensed under the MIT License.
```
