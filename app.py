import time
import streamlit as st
import requests

st.set_page_config(page_title="MCP Weather App", page_icon="🌤️", layout="centered")

st.markdown("""
    <style>
    .main {
        background-color: #f0f8ff;
    }
    .weather-card {
        border-radius: 15px;
        padding: 20px;
        background: #ffffff;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌦️ MCP Weather Explorer")

location = st.text_input("📍 Enter a city or zip code", "New York")

def display_usage_metrics(start_time: float, usage: dict):
    elapsed_time = round(time.time() - start_time, 2)
    prompt_tokens = usage.get("prompt_tokens", 0)
    completion_tokens = usage.get("completion_tokens", 0)
    total_tokens = usage.get("total_tokens", 0)

    st.markdown("---")
    st.markdown("#### 📊 Usage & Performance")
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🕒 Response Time", f"{elapsed_time}s")
    col2.metric("🧠 Prompt Tokens", prompt_tokens)
    col3.metric("💬 Completion Tokens", completion_tokens)
    col4.metric("🔢 Total Tokens", total_tokens)

if st.button("🔍 Get Weather"):
    with st.spinner("Fetching data..."):
        try:
            start_time = time.time()
            response = requests.post("http://localhost:8000/weather", json={"location": location})
            response.raise_for_status()
            data = response.json()

            # Simple condition to emoji mapping
            condition = data.get("condition", "").lower()
            if "sun" in condition:
                icon = "☀️"
            elif "cloud" in condition:
                icon = "☁️"
            elif "rain" in condition:
                icon = "🌧️"
            elif "snow" in condition:
                icon = "❄️"
            else:
                icon = "🌤️"

            st.markdown(f"""
                <div class="weather-card">
                    <h3>{icon} Weather in <span style="color:#0072ff;">{data['location']}</span></h3>
                    <ul>
                        <li><strong>Temperature:</strong> {data['temperature']}</li>
                        <li><strong>Humidity:</strong> {data['humidity']}</li>
                        <li><strong>Air Quality:</strong> {data['air_quality']}</li>
                        <li><strong>Condition:</strong> {data['condition']}</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

            usage = data.get("usage", {})
            print(f"usage in app: {usage}")
            display_usage_metrics(start_time, usage)
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Optional: static footer or credits
st.markdown("<hr><center><sub>Powered by MCP + LLMs + Open Web</sub></center>", unsafe_allow_html=True)

