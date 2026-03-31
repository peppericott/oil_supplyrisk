import pandas as pd

# Load the raw dataset
df = pd.read_csv("data/Crude Oil Production by Country.csv")

# Print to verify
print("Columns:", df.columns.tolist())
print("Shape:", df.shape)

# Drop the Flag column
df = df.drop(columns=["Flag"])

# Rename Country column
df = df.rename(columns={"Country": "country"})

# Keep only country + 2018 production
df = df[["country", "2018"]]
df = df.rename(columns={"2018": "production"})

# Drop rows with missing production
df = df.dropna(subset=["production"])

print("After cleanup:", df.shape)
print(df.head())

# Add latitude and longitude by country
coords = {
    "United States": (37.09, -95.71),
    "Saudi Arabia": (23.89, 45.08),
    "Russia": (61.52, 105.31),
    "Canada": (56.13, -106.34),
    "Iraq": (33.22, 43.68),
    "Iran": (32.43, 53.69),
    "China": (35.86, 104.19),
    "UAE": (23.42, 53.85),
    "Brazil": (-14.24, -51.93),
    "Kuwait": (29.31, 47.48),
    "Mexico": (23.63, -102.55),
    "Nigeria": (9.08, 8.67),
    "Kazakhstan": (48.02, 66.92),
    "Qatar": (25.35, 51.18),
    "Norway": (60.47, 8.47),
    "Angola": (-11.20, 17.87),
    "Algeria": (28.03, 1.66),
    "Venezuela": (6.42, -66.59),
    "U.K.": (55.38, -3.44),
    "Libya": (26.33, 17.23),
    "Oman": (21.51, 55.92),
    "Colombia": (4.57, -74.30),
    "Indonesia": (-0.79, 113.92),
    "Yemen": (15.55, 48.52),
    "Syria": (34.80, 38.99),
    "Sudan": (12.86, 30.22),
    "Azerbaijan": (40.14, 47.58),
    "Malaysia": (4.21, 108.96),
    "Egypt": (26.82, 30.80),
    "Argentina": (-38.42, -63.62),
}

# Recent 2024-2025 geopolitical risk status
risk_status = {
    "Iraq": "disrupted",
    "Iran": "disrupted",
    "Libya": "disrupted",
    "Venezuela": "disrupted",
    "Nigeria": "disrupted",
    "Russia": "disrupted",
    "Yemen": "disrupted",
    "Syria": "disrupted",
    "Sudan": "disrupted",
}

df["latitude"] = df["country"].map(lambda x: coords.get(x, (0, 0))[0])
df["longitude"] = df["country"].map(lambda x: coords.get(x, (0, 0))[1])
df["status"] = df["country"].map(lambda x: risk_status.get(x, "active"))

# Remove countries with no coordinates
df = df[df["latitude"] != 0]

# Save
df.to_csv("data/data.csv", index=False)
print("Done! Sample:")
print(df.head(10))
print("Total countries:", len(df))
