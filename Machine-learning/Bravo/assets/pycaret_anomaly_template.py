"""
Reusable PyCaret anomaly-detection multi-algorithm benchmark.

Run inside an isolated conda env (see SKILL.md "PyCaret" section for why
and how to create one) -- never in a base env with a newer Python/pandas.

Usage: adapt DATA_LOADING, FEATURE_NAMES, LABEL_COL, POSITIVE_LABEL below
to the actual dataset, then run with:
    conda run -n <env_name> python pycaret_anomaly_template.py
"""

from pathlib import Path

import pandas as pd
from pycaret.anomaly import setup, create_model, predict_model, save_model, models

# ---- adapt these to the dataset ----
TRAIN_CSV = Path("features_train.csv")   # majority/normal class only, unsupervised
EVAL_CSV = Path("features_eval.csv")     # has known labels, used only to score after fitting
FEATURE_NAMES = ["feature_1", "feature_2", "feature_3", "feature_4"]
LABEL_COL = "label"
POSITIVE_LABEL = "Anomaly"   # the minority/defect class value in LABEL_COL
CONTAMINATION = 0.05
MODELS_DIR = Path("models")
RESULTS_CSV = Path("anomaly_comparison.csv")
# -------------------------------------


def main():
    train_df = pd.read_csv(TRAIN_CSV)
    eval_df = pd.read_csv(EVAL_CSV)

    setup(data=train_df[FEATURE_NAMES], session_id=42, verbose=False)

    algo_ids = list(models().index)  # pull from PyCaret's own registry, don't hardcode
    results = []

    for algo in algo_ids:
        try:
            model = create_model(algo, fraction=CONTAMINATION)
            scored = predict_model(model, data=eval_df[FEATURE_NAMES])
        except Exception as e:
            # known: 'sod' (pyod) crashes with KeyError on DataFrame input -- not our bug
            print(f"[skip] {algo}: {e}")
            continue

        scored["true_label"] = eval_df[LABEL_COL].values
        pos_mask = scored["true_label"] == POSITIVE_LABEL
        neg_mask = ~pos_mask

        sensitivity = (scored.loc[pos_mask, "Anomaly"] == 1).mean()
        specificity = (scored.loc[neg_mask, "Anomaly"] == 0).mean()

        results.append({
            "algorithm": algo,
            "sensitivity_pct": round(sensitivity * 100, 1),
            "specificity_pct": round(specificity * 100, 1),
        })
        print(f"{algo:10s} sensitivity={sensitivity*100:5.1f}%  specificity={specificity*100:5.1f}%")
        save_model(model, str(MODELS_DIR / f"anomaly_{algo}"))

    results_df = pd.DataFrame(results).sort_values(
        ["sensitivity_pct", "specificity_pct"], ascending=False
    )
    results_df.to_csv(RESULTS_CSV, index=False)
    print("\n=== Comparison ===")
    print(results_df.to_string(index=False))


if __name__ == "__main__":
    main()
