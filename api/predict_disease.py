import tensorflow as tf
import numpy as np
from PIL import Image

# Cache models (performance boost)
model_cache = {}

def load_model(crop):

    if crop not in model_cache:
        try:
            model_cache[crop] = tf.keras.models.load_model(f"models/{crop}_model.h5")
        except:
            return None

    return model_cache[crop]


def predict_disease(image, crop, class_names):

    crop = crop.lower()

    model = load_model(crop)

    if model is None:
        return "Model not available", 0

    img = image.resize((224,224))
    img = np.array(img)/255.0
    img = np.expand_dims(img, axis=0)

    preds = model.predict(img)

    index = np.argmax(preds)
    confidence = preds[0][index]

    return class_names[index], float(confidence)