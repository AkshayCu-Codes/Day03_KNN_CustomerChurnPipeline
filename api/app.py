from fastapi import FastAPI
import joblib, pandas as pd

app = FastAPI(title="Churn Prediction API")

model = joblib.load("E:\AIML\Day03_KNN_CustomerChurn\model\churn_knn_pipeline.pkl")

@app.post("/predict")
def predict(data: dict):
    df = pd.DataFrame([data])
    result = model.predict(df)[0]
    return {"prediction": int(result), "message": "Likely to Leave" if result == 1 else "Likely to Stay"}
