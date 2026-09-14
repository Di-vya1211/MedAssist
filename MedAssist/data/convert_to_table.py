import json
import pandas as pd

with open("data/medassist_complete.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

for column in ["also_called", "sections", "groups"]:
    if column in df.columns:
        df[column] = df[column].apply(
            lambda x: ", ".join(x) if isinstance(x, list) else x
        )

df.to_csv("medical_data.csv", index=False)

print("Done! Table CSV file mein convert ho gayi.")
print(df.head())