from pathlib import Path

import pandas as pd
from ydata_profiling import ProfileReport


project_root = Path(__file__).resolve().parent.parent
data_path = project_root / "data" / "raw" / "stix_flares.csv"

print("CSV-Pfad:", data_path)
print("CSV vorhanden:", data_path.exists())

df = pd.read_csv(data_path)

print(f"Beobachtungen: {df.shape[0]}")
print(f"Merkmale: {df.shape[1]}")

report_path = (
    project_root
    / "data analysis"
    / "stix_profile_report.html"
)

profile = ProfileReport(
    df,
    title="STIX Solar Flares – Data Profile",
    minimal=True
)

profile.to_file(report_path)

print("Bericht gespeichert:", report_path)