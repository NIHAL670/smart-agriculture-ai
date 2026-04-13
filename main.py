from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from PIL import Image

from api.predict_crop import predict_crop, predict_crop_proba
from utils.fertilizer_engine import recommend_fertilizer
from utils.water_calc import water_requirement
from api.predict_disease import predict_disease
from utils.class_names import class_names_map

app = FastAPI()

class CropRequest(BaseModel):
    N: float
    P: float
    K: float
    temp: float
    humidity: float
    ph: float
    rainfall: float
    land_area: float

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict-all")
def predict_all(data: CropRequest):

    # validation
    if data.N == 0 or data.P == 0 or data.K == 0 or data.temp == 0:
        return {"error": "Invalid input"}

    # crop
    crop = predict_crop(
        data.N, data.P, data.K,
        data.temp, data.humidity,
        data.ph, data.rainfall
    )

    crop = crop.lower()

    top_crops = predict_crop_proba(
        data.N, data.P, data.K,
        data.temp, data.humidity,
        data.ph, data.rainfall
    )

    top_crops = [
        {"crop": c[0], "probability": float(c[1])}
        for c in top_crops
    ]

    fertilizer = recommend_fertilizer(
        data.N, data.P, data.K,
        crop, data.land_area
    )

    water = water_requirement(
        crop, data.land_area,
        data.temp, data.humidity,
        data.rainfall
    )

    return {
        "recommended_crop": crop,
        "top_crops": top_crops,
        "fertilizer": fertilizer,
        "water": water
    }

@app.post("/predict-disease")
async def detect_disease(file: UploadFile = File(...), crop_type: str = "tomato"):

    image = Image.open(file.file)

    disease, confidence = predict_disease(
        image,
        crop_type,
        class_names_map[crop_type]
    )

    return {
        "disease": disease,
        "confidence": float(confidence)
    }
