# ml/explore.py
import pandas as pd
import numpy as np

df = pd.read_csv("data/raw/triage.csv")

print("=== شکل دیتاست ===")
print(df.shape)

print("\n=== ستون‌ها ===")
print(df.columns.tolist())

print("\n=== نمونه اول ===")
print(df.head(2))

print("\n=== نوع داده‌ها ===")
print(df.dtypes)

print("\n=== مقادیر خالی ===")
print(df.isnull().sum()[df.isnull().sum() > 0])

print("\n=== ستون هدف (احتمالی) ===")
# دنبال ستونی با کلمه triage یا acuity یا priority می‌گردیم
target_candidates = [c for c in df.columns if any(
    k in c.lower() for k in ["triage", "acuity", "priority", "level", "esi"]
)]
print(target_candidates)
for col in target_candidates:
    print(f"\n{col}:\n{df[col].value_counts()}")
