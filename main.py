from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
from utils import calculate_risk, to_geojson
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_data():
   BASE_DIR = os.path.dirname(os.path.abspath(__file__))
   file_path = os.path.join(BASE_DIR, "data.csv")
   df = pd.read_csv(file_path)
   df.columns = df.columns.str.lower()
   return df

@app.get("/")
def home():
    return {"message": "Global Risk API is running"}

@app.get("/data")
def get_data():
    df = load_data()
    return df.to_dict(orient='records')

@app.get("/live-data")
def live_data():
    df = load_data()
    results = []
    for _, row in df.iterrows():
        risk, reasons = calculate_risk(row)
        item = row.to_dict()
        item["risk"] = risk
        item["ai_reason"] = str(reasons)

        if risk >= 10:
            item["risk_level"] = "Critical"
        elif risk >= 7:
            item["risk_level"] = "High"
        elif risk >= 4:
            item["risk_level"] = "Medium"
        else:
            item["risk_level"] = "Low"

        results.append(item)
    return results

@app.get("/geojson")
def geojson():
    df = load_data()
    return to_geojson(df)