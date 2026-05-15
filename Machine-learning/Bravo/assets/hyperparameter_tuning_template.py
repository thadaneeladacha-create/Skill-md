"""
Hyperparameter Tuning Template
ใช้ GridSearchCV หรือ RandomizedSearchCV สำหรับหา hyperparameter ที่ดีที่สุด
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from scipy.stats import randint, uniform

# from preprocessing_template import preprocessor, X_train, y_train

RANDOM_STATE = 42


# ---------- ตัวอย่างที่ 1: GridSearchCV (เหมาะกับ param ไม่เยอะ) ----------
def grid_search_rf(preprocessor, X_train, y_train, cv=5):
    """หา hyperparameter ของ Random Forest แบบ exhaustive"""
    pipe = Pipeline([
        ("preprocessor", preprocessor),
        ("model", RandomForestClassifier(random_state=RANDOM_STATE)),
    ])

    param_grid = {
        "model__n_estimators": [100, 200, 500],
        "model__max_depth": [None, 10, 20, 30],
        "model__min_samples_split": [2, 5, 10],
        "model__min_samples_leaf": [1, 2, 4],
    }

    grid_search = GridSearchCV(
        pipe,
        param_grid,
        cv=cv,
        scoring="f1_weighted",
        n_jobs=-1,
        verbose=2,
    )
    grid_search.fit(X_train, y_train)

    print(f"\nBest score: {grid_search.best_score_:.4f}")
    print(f"Best params: {grid_search.best_params_}")
    return grid_search.best_estimator_


# ---------- ตัวอย่างที่ 2: RandomizedSearchCV (เร็วกว่า, ครอบคลุมกว่า) ----------
def random_search_rf(preprocessor, X_train, y_train, n_iter=50, cv=5):
    """หา hyperparameter ของ Random Forest แบบสุ่ม"""
    pipe = Pipeline([
        ("preprocessor", preprocessor),
        ("model", RandomForestClassifier(random_state=RANDOM_STATE)),
    ])

    param_distributions = {
        "model__n_estimators": randint(50, 500),
        "model__max_depth": [None, 5, 10, 20, 30, 50],
        "model__min_samples_split": randint(2, 20),
        "model__min_samples_leaf": randint(1, 10),
        "model__max_features": ["sqrt", "log2", 0.3, 0.5, 0.7],
    }

    random_search = RandomizedSearchCV(
        pipe,
        param_distributions,
        n_iter=n_iter,
        cv=cv,
        scoring="f1_weighted",
        n_jobs=-1,
        random_state=RANDOM_STATE,
        verbose=2,
    )
    random_search.fit(X_train, y_train)

    print(f"\nBest score: {random_search.best_score_:.4f}")
    print(f"Best params: {random_search.best_params_}")
    return random_search.best_estimator_


# ---------- ตัวอย่างที่ 3: ใช้ Optuna (Bayesian Optimization) ----------
# import optuna
#
# def objective(trial):
#     n_estimators = trial.suggest_int("n_estimators", 50, 500)
#     max_depth = trial.suggest_int("max_depth", 3, 50)
#     min_samples_split = trial.suggest_int("min_samples_split", 2, 20)
#
#     model = RandomForestClassifier(
#         n_estimators=n_estimators,
#         max_depth=max_depth,
#         min_samples_split=min_samples_split,
#         random_state=RANDOM_STATE,
#     )
#     pipe = Pipeline([("preprocessor", preprocessor), ("model", model)])
#     scores = cross_val_score(pipe, X_train, y_train, cv=5, scoring="f1_weighted")
#     return scores.mean()
#
# study = optuna.create_study(direction="maximize")
# study.optimize(objective, n_trials=100)
# print(study.best_params)


# ---------- ตัวอย่างการเรียกใช้ ----------
# best_model = random_search_rf(preprocessor, X_train, y_train, n_iter=30)
# # จากนั้นนำ best_model ไปประเมินบน test set
