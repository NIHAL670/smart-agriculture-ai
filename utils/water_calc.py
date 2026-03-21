def water_requirement(crop, land_area, temperature, humidity, rainfall):

    crop = crop.lower()

    # Base crop water need (mm/day)
    crop_water = {
        "rice": 5.5,
        "wheat": 4.0,
        "maize": 3.5,
        "cotton": 6.0,
        "banana": 6.5
    }

    if crop not in crop_water:
        return "No data available"

    base_mm = crop_water[crop]

    # Climate adjustment
    if temperature > 30:
        base_mm += 1

    if humidity < 50:
        base_mm += 0.5

    if rainfall > 5:
        base_mm -= 1

    # Convert mm → liters
    # 1 mm = 10,000 L per hectare
    liters_per_hectare = base_mm * 10000

    total_water = liters_per_hectare * land_area

    return {
        "per_hectare": f"{round(liters_per_hectare)} L/day",
        "total": f"{round(total_water)} L/day"
    }