def calculate_risk(row):
    risk = 0
    reasons = []

    # Strait of Hormuz chokepoint countries
    if row.get("country") in ["Iran", "Iraq", "UAE", "Qatar", "Kuwait", "Oman"]:
        risk += 4
        reasons.append("Near Strait of Hormuz chokepoint")

    # Active conflict zones 2024-2025
    if row.get("country") in ["Russia", "Libya", "Sudan", "Yemen", "Syria"]:
        risk += 5
        reasons.append("Active conflict zone")

    # Houthi/Red Sea shipping disruption
    if row.get("country") in ["Yemen", "Iran"]:
        risk += 3
        reasons.append("Houthi/Red Sea shipping threat")

    # Major international sanctions
    if row.get("country") in ["Iran", "Russia", "Venezuela"]:
        risk += 3
        reasons.append("Major international sanctions")

    # Low production capacity
    if float(row.get("production", 100)) < 500:
        risk += 2
        reasons.append("Low production capacity")

    # Operational disruption status
    if str(row.get("status", "")).lower() == "disrupted":
        risk += 2
        reasons.append("Operational disruption")

    # Risk level label
    if risk >= 10:
        risk_level = "Critical"
    elif risk >= 7:
        risk_level = "High"
    elif risk >= 4:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    reasons.append(f"Risk Level: {risk_level}")

    return risk, reasons


def to_geojson(df):
    features = []

    for _, row in df.iterrows():
        risk, reasons = calculate_risk(row)

        features.append({
            "type": "Feature",
            "properties": {
                **row.to_dict(),
                "risk": risk,
                "risk_level": reasons[-1].replace("Risk Level: ", ""),
                "ai_reason": reasons[:-1]
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    float(row.get("longitude", 0)),
                    float(row.get("latitude", 0))
                ]
            }
        })

    return {
        "type": "FeatureCollection",
        "features": features
    }