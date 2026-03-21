def recommend_fertilizer(N, P, K, crop, land_area):

    crop = crop.lower()

    # Ideal nutrient requirement (kg/ha)
    crop_req = {
        "rice": {"N": 120, "P": 60, "K": 40},
        "wheat": {"N": 100, "P": 50, "K": 30},
        "maize": {"N": 110, "P": 50, "K": 35},
        "cotton": {"N": 120, "P": 60, "K": 60},
        "banana": {"N": 200, "P": 60, "K": 200}
    }

    if crop not in crop_req:
        return "No data available"

    req = crop_req[crop]

    # Deficit calculation
    N_def = max(req["N"] - N, 0)
    P_def = max(req["P"] - P, 0)
    K_def = max(req["K"] - K, 0)

    result = []

    # Urea (46% N)
    if N_def > 0:
        urea = N_def / 0.46
        result.append(f"Urea: {round(urea,1)} kg/ha")

    # DAP (18% N, 46% P)
    if P_def > 0:
        dap = P_def / 0.46
        result.append(f"DAP: {round(dap,1)} kg/ha")

    # MOP (60% K)
    if K_def > 0:
        mop = K_def / 0.60
        result.append(f"MOP: {round(mop,1)} kg/ha")

    if not result:
        return "Soil nutrients are sufficient"

    # Calculate for total land
    total_result = []
    for item in result:
        name, value = item.split(":")
        value = float(value.split()[0])
        total = value * land_area
        total_result.append(f"{name}: {round(total,1)} kg total")

    return {
        "per_hectare": result,
        "total": total_result
    }