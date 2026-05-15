"""
Classification Model Template
ลองหลายโมเดลและเปรียบเทียบผลด้วย cross-validation
"""

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.dummy import DummyClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score, StratifiedKFold

# import preprocessor จาก preprocessing_template.py
# from preprocessing_template import preprocessor, X_train, X_test, y_train, y_test

RANDOM_STATE = 42


# ---------- สร้าง dict ของโมเดลที่จะเปรียบเทียบ ----------
models = {
    "Baseline (most_frequent)": DummyClassifier(strategy="most_frequent"),
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE),
    "Gradient Boosting": GradientBoostingClassifier(random_state=RANDOM_STATE),
    "SVM (RBF)": SVC(kernel="rbf", probability=True, random_state=RANDOM_STATE),
}


# ---------- เปรียบเทียบด้วย Cross-Validation ----------
def compare_models(models, preprocessor, X, y, cv=5, scoring="f1_weighted"):
    """ฝึกและประเมินโมเดลด้วย Stratified K-Fold CV"""
    results = []
    skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=RANDOM_STATE)

    for name, model in models.items():
        pipe = Pipeline([
            ("preprocessor", preprocessor),
            ("model", model),
        ])
        scores = cross_val_score(pipe, X, y, cv=skf, scoring=scoring, n_jobs=-1)
        results.append({
            "model": name,
            "mean_score": scores.mean(),
            "std_score": scores.std(),
        })
        print(f"{name:30s} {scoring}: {scores.mean():.4f} (±{scores.std():.4f})")

    return pd.DataFrame(results).sort_values("mean_score", ascending=False)


# ---------- ตัวอย่างการเรียกใช้ ----------
# results_df = compare_models(models, preprocessor, X_train, y_train, cv=5)
# print("\nผลการเปรียบเทียบ:")
# print(results_df)


# ---------- เลือกโมเดลที่ดีที่สุดและ fit บน train ทั้งหมด ----------
def train_best_model(model, preprocessor, X_train, y_train):
    """train โมเดลที่เลือกแล้วบน train set ทั้งหมด"""
    pipe = Pipeline([
        ("preprocessor", preprocessor),
        ("model", model),
    ])
    pipe.fit(X_train, y_train)
    return pipe
