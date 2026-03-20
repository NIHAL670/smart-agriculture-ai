import streamlit as st
from api.predict_crop import predict_crop
from utils.fertilizer_engine import recommend_fertilizer
from utils.water_calc import water_requirement
from api.predict_crop import predict_crop, predict_crop_proba

st.markdown("""
<style>

/* Background Gradient */
.stApp {
    background:
      radial-gradient(1200px 600px at 15% 10%, rgba(0, 255, 204, 0.18), transparent 55%),
      radial-gradient(900px 500px at 85% 15%, rgba(0, 114, 255, 0.22), transparent 55%),
      radial-gradient(900px 600px at 70% 90%, rgba(173, 0, 255, 0.16), transparent 60%),
      linear-gradient(135deg, #0b1220 0%, #0f1b2e 45%, #101026 100%);
    color: white;
}

/* Glass Card */
.glass {
    position: relative;
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.14),
      rgba(255, 255, 255, 0.06)
    );
    backdrop-filter: blur(18px) saturate(140%);
    -webkit-backdrop-filter: blur(18px) saturate(140%);
    border-radius: 18px;
    padding: 20px;
    margin: 10px 0;
    border: 1px solid rgba(255, 255, 255, 0.22);
    box-shadow:
      0 12px 28px rgba(0, 0, 0, 0.35),
      inset 0 1px 0 rgba(255, 255, 255, 0.12);
    transition: transform 180ms ease, box-shadow 220ms ease, border-color 220ms ease;
}

/* Card Glow on Hover */
.glass:hover {
    transform: translateY(-2px);
    border-color: rgba(0, 255, 204, 0.35);
    box-shadow:
      0 16px 40px rgba(0, 0, 0, 0.45),
      0 0 0 1px rgba(0, 255, 204, 0.18),
      0 0 28px rgba(0, 255, 204, 0.22),
      0 0 60px rgba(0, 114, 255, 0.14),
      inset 0 1px 0 rgba(255, 255, 255, 0.14);
}

/* Alternate Glass (orange tint) */
.glass-alt {
    background: linear-gradient(
      135deg,
      rgba(255, 167, 38, 0.16),
      rgba(255, 255, 255, 0.06)
    );
    border-color: rgba(255, 167, 38, 0.22);
}

/* System features: glassy multi-color labels */
.features-title {
    margin: 0 0 0.35rem 0;
    display: inline-block;
    background-image: linear-gradient(90deg, rgba(255, 77, 109, 0.98), rgba(255, 34, 87, 0.92), rgba(255, 167, 38, 0.75));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent !important;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 10px 34px rgba(255, 34, 87, 0.14), 0 14px 46px rgba(255, 77, 109, 0.12);
}

.feature-item {
    font-weight: 600;
    letter-spacing: 0.2px;
    background-clip: text;
    -webkit-background-clip: text;
    color: transparent;
    text-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
}

.feature-1 {
    background-image: linear-gradient(90deg, rgba(0, 255, 204, 0.95), rgba(0, 114, 255, 0.95));
    text-shadow: 0 10px 34px rgba(0, 255, 204, 0.12), 0 14px 46px rgba(0, 114, 255, 0.12);
}

.feature-2 {
    background-image: linear-gradient(90deg, rgba(255, 167, 38, 0.98), rgba(255, 99, 132, 0.92));
    text-shadow: 0 10px 34px rgba(255, 167, 38, 0.14), 0 14px 46px rgba(255, 99, 132, 0.12);
}

.feature-3 {
    background-image: linear-gradient(90deg, rgba(173, 0, 255, 0.92), rgba(47, 129, 247, 0.95));
    text-shadow: 0 10px 34px rgba(173, 0, 255, 0.12), 0 14px 46px rgba(47, 129, 247, 0.14);
}

/* Input boxes */
input, .stNumberInput input {
    background-color: rgba(255,255,255,0.1) !important;
    color: white !important;
    border-radius: 10px !important;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    border: none;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #0072ff, #00c6ff);
}

/* Titles */
h1 {
    background: linear-gradient(
      90deg,
      rgba(10, 28, 76, 0.98),
      rgba(16, 58, 140, 0.98),
      rgba(0, 114, 255, 0.92)
    );
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    text-shadow: 0 6px 24px rgba(0, 114, 255, 0.18), 0 10px 40px rgba(16, 58, 140, 0.18);
}

h2, h3 {
    color: #ffffff;
}

</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Smart Agriculture AI",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 Smart Agriculture AI System")
st.markdown("AI Powered Crop Recommendation & Farm Assistance")

st.markdown("## 🧾 Enter Farm Details")

col1, col2, col3 = st.columns(3)

with col1:
   N = st.number_input("Nitrogen (N)", 0, 200, value=70)
   P = st.number_input("Phosphorus (P)", 0, 200, value=80)
   K = st.number_input("Potassium (K)", 0, 200, value=90)
with col2:
    ph = st.number_input("Soil pH", 0.0, 14.0)
    temp = st.number_input("Temperature (°C)")
    humidity = st.number_input("Humidity (%)")

with col3:
    rainfall = st.number_input("Rainfall (mm)")
    land_area = st.number_input("Land Area (hectare)", 1)



predict_button = st.button("🔍 Predict", use_container_width=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🌱 Crop Recommendation")

with col2:
    st.subheader("🧪 Fertilizer Suggestion")

with col3:
    st.subheader("💧 Water Requirement")

import matplotlib.pyplot as plt
from api.predict_crop import predict_crop, predict_crop_proba

# 🔘 Predict Button
if predict_button:

    # ✅ Input validation
    if N == 0 or P == 0 or K == 0 or ph == 0 or temp == 0 or humidity == 0:
        st.error("⚠️ Please enter valid inputs")
    
    else:

        # 🌱 Crop prediction
        crop = predict_crop(N, P, K, temp, humidity, ph, rainfall)
        crop = crop.lower()

        # 📊 Top 3 crops
        top_crops = predict_crop_proba(N, P, K, temp, humidity, ph, rainfall)

        crops = [c[0] for c in top_crops]
        probs = [c[1] for c in top_crops]

        # 🌱 Show best crop
        with col1:
            st.markdown('<div class="glass">', unsafe_allow_html=True)

            st.markdown("### 🌱 Crop Recommendation")

            st.markdown(f"""
            <h2 style='text-align:center; color:#00ffcc;'>
            {crop.upper()}
            </h2>
            """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        # 🧪 Fertilizer
        fertilizer = recommend_fertilizer(N, P, K, crop, land_area)

        with col2:
            if isinstance(fertilizer, dict):
                st.info("Per Hectare:\n" + "\n".join(fertilizer["per_hectare"]))
                st.info("Total:\n" + "\n".join(fertilizer["total"]))
            else:
                st.info(fertilizer)

        # 💧 Water
        water = water_requirement(crop, land_area, temp, humidity, rainfall)

        with col3:
            if isinstance(water, dict):
                st.warning(f"Per Hectare: {water['per_hectare']}")
                st.warning(f"Total: {water['total']}")
            else:
                st.warning(water)

        # 📊 GRAPH (IMPORTANT — inside button)
        st.markdown("### 📊 Top 3 Crop Predictions")

        fig, ax = plt.subplots()
        colors = plt.cm.viridis([0.25, 0.55, 0.85])
        ax.bar(crops, probs, color=colors, edgecolor="white", linewidth=0.8)
        ax.set_facecolor((1, 1, 1, 0))
        fig.patch.set_alpha(0)

        label_blue = "#2f81f7"
        ax.set_title("Top Crop Recommendations", color=label_blue)
        ax.set_ylabel("Confidence Score", color=label_blue)
        ax.set_ylim(0, 1)
        ax.grid(axis="y", linestyle="--", alpha=0.25)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.tick_params(axis="x", colors=label_blue)
        ax.tick_params(axis="y", colors=label_blue)

        for i, v in enumerate(probs):
            ax.text(i, v + 0.02, f"{round(v,2)}", ha='center', color=label_blue)

        st.pyplot(fig)
    

st.markdown('<div class="glass glass-alt features">', unsafe_allow_html=True)
st.markdown('<h3 class="features-title">📊 System Features</h3>', unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)

st.markdown("## 📸 Crop Disease Detection")

from api.predict_disease import predict_disease
from utils.class_names import class_names_map
from PIL import Image
# 🔽 ADD HERE
disease_solutions = {
    "Late Blight": {
        "description": "A fast-spreading fungal disease that occurs in moist conditions.",
        "solution": [
            "Apply copper-based fungicide",
            "Remove infected leaves",
            "Ensure proper drainage"
        ]
    },
    "Early Blight": {
        "description": "Causes target-like brown spots on leaves.",
        "solution": [
            "Use crop rotation",
            "Apply neem oil or fungicide",
            "Maintain soil nutrients"
        ]
    },
    "Healthy": {
        "description": "Plant is healthy with no disease.",
        "solution": [
            "Maintain regular watering",
            "Use balanced fertilizer",
            "Monitor plant regularly"
        ]
    }
}

# Crop select
crop_type = st.selectbox(
    "Select Crop",
    ["rice", "maize", "cotton", "banana", "tomato", "potato"]
)

# Upload
uploaded_file = st.file_uploader("Upload Leaf Image", type=["jpg","png"])

# 👇 IMPORTANT — yahi logic missing tha
if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.image(image, caption="Uploaded Image")

    # 👉 BUTTON CENTER ME
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        detect_button = st.button("🔬 Detect Disease", use_container_width=True)

    # 👉 BUTTON CLICK PAR RUN
    if detect_button:

        with st.spinner("Analyzing image..."):

            disease, confidence = predict_disease(
                image,
                crop_type,
                class_names_map[crop_type]
            )

            st.markdown('<div class="glass">', unsafe_allow_html=True)

            st.subheader("🦠 Disease Analysis")

            st.success(f"{disease}")
            st.write(f"Confidence: {round(confidence*100,2)}%")
            # 🔽 ADD HERE
        info = disease_solutions.get(disease)

        if info:
         st.subheader("📖 Description")
         st.write(info["description"])

         st.subheader("💊 Recommended Actions")
         for sol in info["solution"]:
          st.write(f"✔ {sol}")

          st.markdown('</div>', unsafe_allow_html=True)
with col4:
    st.markdown('<span class="feature-item feature-1">✔ Weather Based Crop Prediction</span>', unsafe_allow_html=True)

with col5:
    st.markdown('<span class="feature-item feature-2">✔ Soil Nutrient Analysis</span>', unsafe_allow_html=True)

with col6:
    st.markdown('<span class="feature-item feature-3">✔ Fertilizer & Irrigation Recommendation</span>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("---")

st.caption("Developed using Machine Learning + Weather API + Streamlit and created with ❤️ by NIHAL YADAV")

