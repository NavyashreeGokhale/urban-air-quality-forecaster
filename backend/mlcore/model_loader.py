import pickle
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "aqi_model.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

def predict_aqi(features):

    if len(features) != 6:
        raise ValueError("Model expects exactly 6 features") 
    
    prediction = model.predict([features])
    return float(prediction[0])