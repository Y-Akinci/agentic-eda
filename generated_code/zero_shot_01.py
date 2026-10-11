import os

import matplotlib.pyplot as plt
import pandas as pd


# Create output directory if it does not exist
os.makedirs("outputs/zero_shot_01", exist_ok=True)

# Load the data
df = pd.read_csv("data/raw/stix_flares.csv")

# Convert peak_UTC to datetime
df["peak_UTC"] = pd.to_datetime(df["peak_UTC"])

# Keep February 2021 through February 2026
df = df[
    (df["peak_UTC"] >= pd.Timestamp("2021-02-01"))
    & (df["peak_UTC"] < pd.Timestamp("2026-03-01"))
]

# Drop rows with missing GOES class
df = df[df["GOES_class_time_of_flare"].notnull()]

# Mark M and X flares as strong
df["strong"] = df["GOES_class_time_of_flare"].apply(
    lambda value: 1 if value.upper() in ["M", "X"] else 0
)

# Create month labels
df["month_str"] = df["peak_UTC"].dt.strftime("%Y-%m")

# Calculate monthly values
monthly_total = df.groupby("month_str").size()
monthly_strong = df.groupby("month_str")["strong"].sum()

results = pd.DataFrame(
    {
        "month": monthly_total.index,
        "total_flares": monthly_total,
        "strong_flares": monthly_strong,
        "strong_percentage": (monthly_strong / monthly_total) * 100,
    }
)

# Print key results
print(f"Total flares in period: {df.shape[0]}")
print(f"Total strong flares: {df['strong'].sum()}")
print(
    f"First month: {results.iloc[0]['month']}, "
    f"total flares: {results.iloc[0]['total_flares']}"
)
print(
    f"Last month: {results.iloc[-1]['month']}, "
    f"total flares: {results.iloc[-1]['total_flares']}"
)
print(
    "Strong percentage in first month: "
    f"{results.iloc[0]['strong_percentage']:.2f}%"
)
print(
    "Strong percentage in last month: "
    f"{results.iloc[-1]['strong_percentage']:.2f}%"
)

# Save the plot
plt.figure(figsize=(10, 6))
plt.plot(
    results["month"],
    results["strong_percentage"],
    marker="o",
    linestyle="-",
)
plt.title("Percentage of Strong Flares (M and X) over Time")
plt.xlabel("Month")
plt.ylabel("Percentage (%)")
plt.grid(True)
plt.savefig("outputs/zero_shot_01/strong_flare_percentage.png")
plt.close()