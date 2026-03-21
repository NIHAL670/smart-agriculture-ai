import requests

API_KEY = "66a651f68b751eae54dedbcc8cfa5421"

def get_weather(lat, lon):

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]

    rainfall = 0
    if "rain" in data:
        rainfall = data["rain"].get("1h", 0)

    return {
        "temperature": temperature,
        "humidity": humidity,
        "rainfall": rainfall
    }