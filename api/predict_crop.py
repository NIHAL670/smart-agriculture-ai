import pickle
import numpy as np

model = pickle.load(open("models/crop_model.pkl", "rb"))

# ✅ Single crop
def predict_crop(N, P, K, temp, humidity, ph, rainfall):

    features = np.array([[N, P, K, temp, humidity, ph, rainfall]])
    prediction = model.predict(features)

    return prediction[0]


# ✅ Top 3 crops (for graph)
def predict_crop_proba(N, P, K, temp, humidity, ph, rainfall):

    features = np.array([[N, P, K, temp, humidity, ph, rainfall]])

    probs = model.predict_proba(features)[0]
    crops = model.classes_

    top_indices = probs.argsort()[-3:][::-1]

    top_crops = [(crops[i], probs[i]) for i in top_indices]

    return top_crops