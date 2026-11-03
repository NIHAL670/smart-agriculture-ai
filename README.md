# 🌾 Smart Agriculture AI System

An end-to-end decision-support tool for farmers: it recommends **which crop to grow** from soil and weather conditions, works out **fertiliser and irrigation needs**, and **detects leaf diseases** from a photo.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=flat-square&logo=tensorflow&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)

---

## What it does

| Module | Input | Output | Model |
|---|---|---|---|
| **Crop recommendation** | Soil N, P, K, pH + temperature, humidity, rainfall (7 features) | Best crop + calibrated **top-3** with probabilities, across **22 crops** | Random Forest (scikit-learn) |
| **Fertiliser optimisation** | Soil N, P, K, crop, land area | Urea / DAP / MOP quantities from the nutrient deficit | Rule-based agronomy engine |
| **Irrigation estimate** | Crop, land area, temperature, humidity, rainfall | Daily water requirement (litres/day) | Climate-adjusted crop water model |
| **Leaf-disease detection** | Leaf photo + crop type | Disease class + confidence | One CNN per crop (TensorFlow/Keras), 224×224 input |

Disease detection covers **6 crops**, 3 classes each:

| Crop | Classes |
|---|---|
| Tomato | Early Blight · Late Blight · Healthy |
| Potato | Early Blight · Late Blight · Healthy |
| Rice | Blast · Brown Spot · Healthy |
| Maize | Common Rust · Leaf Blight · Healthy |
| Cotton | Bacterial Blight · Leaf Curl · Healthy |
| Banana | Panama Disease · Sigatoka · Healthy |

## Results

| Model | Metric |
|---|---|
| Crop recommender | **89%** test accuracy |
| Leaf-disease CNNs | **92%** validation accuracy (≈4,000 images across 6 crops) |

## Architecture

```
          ┌──────────────────────────┐
          │  Streamlit dashboard     │  dashboard.py
          │  (inputs, charts, upload)│
          └────────────┬─────────────┘
                       │ calls
     ┌─────────────────┼──────────────────┐
     ▼                 ▼                  ▼
api/predict_crop   utils/fertilizer   api/predict_disease
 (Random Forest)    utils/water_calc   (per-crop CNNs, cached)
     ▲                                    ▲
     └────────── FastAPI service ─────────┘
                   main.py
        /health · /predict-all · /predict-disease
```

## Repository layout

```
├── main.py                 # FastAPI service
├── dashboard.py            # Streamlit UI
├── app.py                  # CLI demo: live weather → crop, fertiliser, water
├── api/
│   ├── predict_crop.py     # crop + top-3 prediction
│   └── predict_disease.py  # per-crop CNN loading (cached) and inference
├── utils/
│   ├── class_names.py      # disease labels per crop
│   ├── fertilizer_engine.py
│   ├── water_calc.py
│   └── weather_api.py      # OpenWeatherMap client (key from env var)
├── crop_model.pkl          # trained crop recommender
└── *_model.h5              # trained disease CNNs (one per crop)
```

## Quick start

```bash
git clone https://github.com/NIHAL670/smart-agriculture-ai.git
cd smart-agriculture-ai
pip install -r requirements.txt

# Dashboard
streamlit run dashboard.py

# REST API (docs at http://localhost:10000/docs)
uvicorn main:app --port 10000
```

The CLI demo in `app.py` fetches live weather, so it needs an [OpenWeatherMap](https://openweathermap.org/api) key:

```bash
export OPENWEATHER_API_KEY="your-key"
python app.py
```

## API

**`POST /predict-all`**

```json
{ "N": 90, "P": 42, "K": 43, "temp": 25.5, "humidity": 80, "ph": 6.5, "rainfall": 200, "land_area": 2 }
```

Returns the recommended crop, top-3 crops with probabilities, a fertiliser plan and the daily water requirement.

**`POST /predict-disease?crop_type=tomato`** — multipart upload with a `file` field (leaf image). Returns `{ "disease": "...", "confidence": 0.97 }`.

## Limitations & next steps

- Fertiliser and irrigation rules currently cover rice, wheat, maize, cotton and banana; other crops return "No data available".
- Disease models expect a clear, single-leaf photo; field images with clutter reduce confidence.
- Planned: confusion matrices per crop, input validation ranges, and a Docker image for one-command deployment.

## Author

**Nihal Yadav** — M.Tech AI & ML, IIT Delhi · [GitHub](https://github.com/NIHAL670) · [LinkedIn](https://linkedin.com/in/nihal-yadav-5131582b8)
