from utils.weather_api import get_weather
from api.predict_crop import predict_crop
from utils.fertilizer_engine import recommend_fertilizer

fertilizer = recommend_fertilizer(N, P, K, crop)

print("Recommended Fertilizer:", fertilizer)
from utils.water_calc import water_requirement

land_area = 2

water = water_requirement(crop, land_area)

print("Water Requirement:", water, "liters/day")

#it is the latitude of any  other specific location so you can adjust accordingly  
lat = 25.3176
lon = 82.9739

weather = get_weather(lat, lon)

temperature = weather["temperature"]
humidity = weather["humidity"]
rainfall = weather["rainfall"]

# Example soil data
N = 90
P = 42
K = 43
ph = 6.5

crop = predict_crop(
    N, P, K,
    temperature,
    humidity,
    ph,
    rainfall
)

print("Weather Data:", weather)
print("Recommended Crop:", crop)