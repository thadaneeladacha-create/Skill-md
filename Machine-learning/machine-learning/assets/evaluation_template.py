"""
Evaluation Template
สร้าง report พร้อม metrics และ visualization
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve,
    mean_absolute_error, mean_squared_error, r2_score,
)


# ---------- Classification Evaluation ----------
def evaluate_classification(model, X_test, y_test, class_names=None, save_dir="."):
    """แสดง metrics, confusion matrix, ROC curve สำหรับ classification"""
    preds = model.predict(X_test)
    try:
        probs = model.predict_proba(X_test)
    except AttributeError:
        probs = None

    print("=== Classification Report ===")
    print(classification_report(y_test, preds, target_names=class_names))

    print("\n=== Metrics ===")
    print(f"Accuracy : {accuracy_score(y_test, preds):.4f}")
    print(f"Precision: {precision_score(y_test, preds, average='weighted'):.4f}")
    print(f"Recall   : {recall_score(y_test, preds, average='weighted'):.4f}")
    print(f"F1       : {f1_score(y_test, preds, average='weighted'):.4f}")

    # ---- Confusion Matrix ----
    cm = confusion_matrix(y_test, preds)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=class_names, yticklabels=class_names)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    plt.tight_layout()
    plt.savefig(f"{save_dir}/confusion_matrix.png")
    plt.close()

    # ---- ROC Curve (binary only) ----
    if probs is not None and probs.shape[1] == 2:
        fpr, tpr, _ = roc_curve(y_test, probs[:, 1])
        auc = roc_auc_score(y_test, probs[:, 1])
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, label=f"AUC = {auc:.4f}")
        plt.plot([0, 1], [0, 1], "k--", alpha=0.5)
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("ROC Curve")
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"{save_dir}/roc_curve.png")
        plt.close()
        print(f"ROC-AUC  : {auc:.4f}")


# ---------- Regression Evaluation ----------
def evaluate_regression(model, X_test, y_test, save_dir="."):
    """แสดง metrics และ residual plot สำหรับ regression"""
    preds = model.predict(X_test)
    residuals = y_test - preds

    print("=== Regression Metrics ===")
    print(f"MAE  : {mean_absolute_error(y_test, preds):.4f}")
    print(f"RMSE : {np.sqrt(mean_squared_error(y_test, preds)):.4f}")
    print(f"R²   : {r2_score(y_test, preds):.4f}")

    # ---- Predicted vs Actual ----
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].scatter(y_test, preds, alpha=0.5)
    axes[0].plot([y_test.min(), y_test.max()],
                 [y_test.min(), y_test.max()], "r--")
    axes[0].set_xlabel("Actual")
    axes[0].set_ylabel("Predicted")
    axes[0].set_title("Predicted vs Actual")

    # ---- Residual plot ----
    axes[1].scatter(preds, residuals, alpha=0.5)
    axes[1].axhline(0, color="red", linestyle="--")
    axes[1].set_xlabel("Predicted")
    axes[1].set_ylabel("Residual")
    axes[1].set_title("Residual Plot")

    plt.tight_layout()
    plt.savefig(f"{save_dir}/regression_evaluation.png")
    plt.close()


# ---------- ตัวอย่างการเรียกใช้ ----------
# evaluate_classification(pipe, X_test, y_test, class_names=["neg", "pos"])
# evaluate_regression(pipe, X_test, y_test)
