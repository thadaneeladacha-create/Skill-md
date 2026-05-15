"""
Regression Model Template
สำหรับงานทำนายตัวเลขต่อเนื่อง (continuous target)
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.dummy import DummyRegressor
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score, KFold

# from preprocessing_template import preprocessor, X_train, X_test, y_train, y_test

RANDOM_STATE = 42


# ---------- สร้าง dict ของโมเดลที่จะเปรียบเทียบ ----------
models = {
    "Baseline (mean)": DummyRegressor(strategy="mean"),
    "Linear Regression": LinearRegression(),
    "Ridge": Ridge(alpha=1.0, random_state=RANDOM_STATE),
    "Lasso": Lasso(alpha=0.1, random_state=RANDOM_STATE),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=RANDOM_STATE),
    "Gradient Boosting": GradientBoostingRegressor(random_state=RANDOM_STATE),
}


# ---------- เปรียบเทียบด้วย Cross-Validation ----------
def compare_regression_models(models, preprocessor, X, y, cv=5):
    """
    ฝึกและประเมินโมเดล regression ด้วย K-Fold CV
    คืนค่าทั้ง RMSE และ R²
    """
    results = []
    kf = KFold(n_splits=cv, shuffle=True, random_state=RANDOM_STATE)

    for name, model in models.items():
        pipe = Pipeline([
            ("preprocessor", preprocessor),
            ("model", model),
        ])
        # neg MSE (sklearn ใช้ค่าลบเพื่อให้ "ยิ่งสูงยิ่งดี")
        mse_scores = -cross_val_score(pipe, X, y, cv=kf,
                                       scoring="neg_mean_squared_error", n_jobs=-1)
        rmse_scores = np.sqrt(mse_scores)
        r2_scores = cross_val_score(pipe, X, y, cv=kf, scoring="r2", n_jobs=-1)

        results.append({
            "model": name,
            "rmse_mean": rmse_scores.mean(),
            "rmse_std": rmse_scores.std(),
            "r2_mean": r2_scores.mean(),
            "r2_std": r2_scores.std(),
        })
        print(f"{name:25s}  RMSE: {rmse_scores.mean():.4f} (±{rmse_scores.std():.4f})  "
              f"R²: {r2_scores.mean():.4f}")

    return pd.DataFrame(results).sort_values("rmse_mean")


# ---------- ตัวอย่างการเรียกใช้ ----------
# results_df = compare_regression_models(models, preprocessor, X_train, y_train, cv=5)
# print("\nผลการเปรียบเทียบ:")
# print(results_df)
