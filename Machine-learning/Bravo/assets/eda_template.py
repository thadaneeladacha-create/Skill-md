"""
EDA Template - Exploratory Data Analysis
ใช้สำรวจข้อมูลก่อนเริ่มสร้างโมเดล
ปรับ DATA_PATH และชื่อ column ให้ตรงกับ dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ---------- กำหนดค่า ----------
DATA_PATH = "data/your_dataset.csv"
TARGET_COL = "target"  # ชื่อ column ที่จะทำนาย


# ---------- โหลดข้อมูล ----------
df = pd.read_csv(DATA_PATH)
print(f"Shape: {df.shape}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nData types:\n{df.dtypes}")
print(f"\nFirst 5 rows:\n{df.head()}")


# ---------- ตรวจสอบคุณภาพข้อมูล ----------
print(f"\n=== Missing Values ===")
missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100
print(pd.DataFrame({"count": missing, "percent": missing_pct})
      .query("count > 0")
      .sort_values("count", ascending=False))

print(f"\n=== Duplicates ===")
print(f"Duplicate rows: {df.duplicated().sum()}")

print(f"\n=== Statistical Summary ===")
print(df.describe())


# ---------- แยก numerical กับ categorical ----------
num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
print(f"\nNumerical columns: {num_cols}")
print(f"Categorical columns: {cat_cols}")


# ---------- Distribution ของ target ----------
plt.figure(figsize=(8, 5))
if df[TARGET_COL].dtype in [np.float64, np.int64] and df[TARGET_COL].nunique() > 20:
    sns.histplot(df[TARGET_COL], kde=True)
    plt.title(f"Distribution of {TARGET_COL}")
else:
    df[TARGET_COL].value_counts().plot(kind="bar")
    plt.title(f"Class distribution of {TARGET_COL}")
plt.tight_layout()
plt.savefig("eda_target_distribution.png")
plt.close()


# ---------- Correlation matrix ----------
if len(num_cols) > 1:
    plt.figure(figsize=(12, 8))
    sns.heatmap(df[num_cols].corr(), annot=True, fmt=".2f", cmap="coolwarm", center=0)
    plt.title("Correlation Matrix")
    plt.tight_layout()
    plt.savefig("eda_correlation.png")
    plt.close()


# ---------- Distribution ของ numerical features ----------
n_num = len(num_cols)
if n_num > 0:
    n_cols = 3
    n_rows = (n_num + n_cols - 1) // n_cols
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4 * n_rows))
    axes = axes.flatten() if n_num > 1 else [axes]
    for i, col in enumerate(num_cols):
        sns.histplot(df[col].dropna(), ax=axes[i], kde=True)
        axes[i].set_title(col)
    for j in range(i + 1, len(axes)):
        axes[j].axis("off")
    plt.tight_layout()
    plt.savefig("eda_numerical_distributions.png")
    plt.close()


print("\n✓ EDA เสร็จสิ้น - ดูไฟล์ภาพ eda_*.png")
