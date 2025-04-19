
from pydantic import BaseModel

class WeatherRequest(BaseModel):
    location: str

class WeatherResponse(BaseModel):
    location: str
    temperature: str
    humidity: str
    air_quality: str
    condition: str
