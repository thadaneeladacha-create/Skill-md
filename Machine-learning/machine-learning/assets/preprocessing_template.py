"""
Preprocessing Template
สร้าง Pipeline สำหรับ preprocessing เพื่อป้องกัน data leakage
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


# ---------- กำหนดค่า ----------
DATA_PATH = "data/your_dataset.csv"
TARGET_COL = "target"
TEST_SIZE = 0.2
RANDOM_STATE = 42


# ---------- โหลดข้อมูล ----------
df = pd.read_csv(DATA_PATH)
X = df.drop(columns=[TARGET_COL])
y = df[TARGET_COL]


# ---------- แยกประเภท column ----------
numeric_features = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
categorical_features = X.select_dtypes(include=["object", "category"]).columns.tolist()

print(f"Numeric features: {numeric_features}")
print(f"Categorical features: {categorical_features}")


# ---------- สร้าง Pipeline สำหรับแต่ละประเภท ----------
numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
])


# ---------- รวมเป็น ColumnTransformer ----------
preprocessor = ColumnTransformer([
    ("num", numeric_pipeline, numeric_features),
    ("cat", categorical_pipeline, categorical_features),
])


# ---------- Train/Test Split ----------
# สำหรับ classification ที่ class imbalance ให้ใส่ stratify=y
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
    stratify=y if y.nunique() < 20 else None,
)

print(f"\nTrain shape: {X_train.shape}, Test shape: {X_test.shape}")


# ---------- ตัวอย่างการใช้กับ model ----------
# from sklearn.ensemble import RandomForestClassifier
# full_pipeline = Pipeline([
#     ("preprocessor", preprocessor),
#     ("model", RandomForestClassifier(random_state=RANDOM_STATE)),
# ])
# full_pipeline.fit(X_train, y_train)
# preds = full_pipeline.predict(X_test)


# Export preprocessor สำหรับใช้ในไฟล์อื่น
__all__ = ["preprocessor", "X_train", "X_test", "y_train", "y_test"]
