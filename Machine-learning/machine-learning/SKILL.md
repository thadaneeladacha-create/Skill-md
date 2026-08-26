---
name: machine-learning
description: ใช้ skill นี้ทุกครั้งที่ผู้ใช้ต้องการสร้าง ฝึก ประเมิน หรือ deploy โมเดล Machine Learning ครอบคลุมการเตรียมข้อมูล (data preprocessing), การเลือกอัลกอริทึม (classification, regression, clustering, anomaly detection), การ train model ด้วย scikit-learn / PyTorch / TensorFlow / PyCaret (AutoML), การประเมินผลด้วย metrics ต่าง ๆ (accuracy, F1, RMSE), การทำ hyperparameter tuning, cross-validation รวมถึงการแก้ปัญหา overfitting/underfitting และการสร้าง pipeline สำหรับ ML. ให้ trigger ทันทีเมื่อผู้ใช้พูดถึง "โมเดล", "เทรนโมเดล", "ML", "AI", "predict", "classification", "regression", "neural network", "deep learning", "sklearn", "pycaret", "AutoML", "anomaly detection", "pandas สำหรับ ML", หรือเมื่ออัพโหลด dataset (.csv, .parquet) แล้วถามว่าจะวิเคราะห์/พยากรณ์ยังไง แม้ไม่ได้พูดคำว่า "machine learning" ตรง ๆ ก็ตาม
---

# Machine Learning Skill

Skill นี้รวบรวมแนวทางและ template สำหรับงาน Machine Learning ตั้งแต่เริ่มต้นจนถึงการนำโมเดลไปใช้งานจริง

## วัตถุประสงค์

ช่วยให้ Claude สามารถ:

- เลือกอัลกอริทึมที่เหมาะสมกับโจทย์ (classification, regression, clustering)
- สร้าง pipeline สำหรับเตรียมข้อมูลและฝึกโมเดลอย่างเป็นระบบ
- ใช้ template ใน `assets/` เพื่อลดเวลาในการเขียนโค้ดซ้ำซ้อน
- ประเมินผลโมเดลด้วย metrics ที่ถูกต้องตามประเภทของปัญหา

## ขั้นตอนการทำงาน (Workflow)

ทำงานตามลำดับนี้เพื่อให้ได้ผลลัพธ์ที่มีคุณภาพ:

### 1. ทำความเข้าใจโจทย์ (Problem Framing)

ก่อนเขียนโค้ดใด ๆ ให้ถามผู้ใช้เพื่อชัดเจนใน:

- ประเภทของปัญหา: classification / regression / clustering / time-series
- target variable คืออะไร (ถ้าเป็น supervised learning)
- ขนาดและรูปแบบของ dataset
- เกณฑ์ความสำเร็จ (success criteria) เช่น ต้องการ accuracy ≥ 90% หรือ RMSE ≤ X

### 2. สำรวจข้อมูล (EDA - Exploratory Data Analysis)

ใช้ `assets/eda_template.py` เป็นจุดเริ่มต้น แล้วปรับให้เข้ากับ dataset:

- ตรวจสอบ missing values, duplicates, outliers
- ดู distribution ของแต่ละ feature
- หา correlation ระหว่าง features และ target
- visualize ด้วย histogram, boxplot, scatter plot

### 3. เตรียมข้อมูล (Preprocessing)

ใช้ `assets/preprocessing_template.py` ซึ่งครอบคลุม:

- การจัดการ missing values (imputation)
- การ encode categorical features (One-Hot, Label Encoding)
- การ scale numerical features (StandardScaler, MinMaxScaler)
- การแบ่ง train/validation/test split

แนะนำให้ห่อขั้นตอนทั้งหมดด้วย `sklearn.pipeline.Pipeline` เพื่อป้องกัน data leakage

### 4. ฝึกโมเดล (Training)

ใช้ template ที่เหมาะสมจาก `assets/`:

- `model_classification_template.py` - สำหรับงานจำแนกประเภท
- `model_regression_template.py` - สำหรับงานทำนายตัวเลขต่อเนื่อง
- `model_neural_network_template.py` - สำหรับ deep learning (PyTorch)

เริ่มจากโมเดลพื้นฐาน (Logistic Regression, Random Forest) ก่อนจะข้ามไปใช้โมเดลซับซ้อน เพื่อเป็น baseline เปรียบเทียบ

### 5. ประเมินผล (Evaluation)

เลือก metric ให้ตรงกับโจทย์:

**Classification:**

- Accuracy ใช้ได้เมื่อ class balance
- Precision/Recall/F1 ใช้เมื่อ class imbalance
- ROC-AUC สำหรับ binary classification ที่สนใจ ranking

**Regression:**

- RMSE/MAE สำหรับวัดความผิดพลาด
- R² สำหรับวัดความสามารถในการอธิบาย variance

ใช้ `assets/evaluation_template.py` เพื่อ generate report พร้อม confusion matrix และ visualization

### 6. ปรับ Hyperparameters

ใช้ `GridSearchCV` หรือ `RandomizedSearchCV` กับ cross-validation (ปกติ 5-fold) ดูตัวอย่างใน `assets/hyperparameter_tuning_template.py`

### 7. ตรวจสอบ Overfitting/Underfitting

- เทียบ training score vs validation score
- ถ้า training score >> validation score → overfitting (ลด complexity, เพิ่ม regularization, เพิ่มข้อมูล)
- ถ้าทั้งคู่ต่ำ → underfitting (เพิ่ม complexity, เพิ่ม feature)

## โครงสร้าง assets/

```
assets/
├── eda_template.py                    - template สำหรับสำรวจข้อมูล
├── preprocessing_template.py          - template สำหรับเตรียมข้อมูล
├── model_classification_template.py   - template สำหรับ classification
├── model_regression_template.py       - template สำหรับ regression
├── model_neural_network_template.py   - template สำหรับ deep learning
├── evaluation_template.py             - template สำหรับประเมินผล
├── hyperparameter_tuning_template.py  - template สำหรับ tuning
└── requirements.txt                   - library ที่ต้องใช้
```

อ่าน template ตรง ๆ ด้วย Read tool แล้วปรับให้เข้ากับ dataset ของผู้ใช้ ไม่ต้อง copy เนื้อหาทั้งหมดมาไว้ใน context ถ้าไม่จำเป็น

## หลักการสำคัญ (Best Practices)

**ป้องกัน data leakage** - ทำ preprocessing ภายใน Pipeline หลังจากแบ่ง train/test แล้วเท่านั้น อย่า fit scaler บนข้อมูลทั้งหมดก่อนแบ่ง

**ตั้ง random_state เสมอ** - เพื่อให้ผลลัพธ์ reproducible ผู้ใช้สามารถรันซ้ำได้ผลเหมือนเดิม

**Baseline ก่อน fancy model** - เริ่มจาก dummy classifier หรือ linear model ก่อน เพื่อให้รู้ว่าโมเดลซับซ้อนนั้นดีกว่าจริง ๆ ไม่ใช่แค่ดูเท่

**บันทึก experiment** - log hyperparameters, metrics, และ data version ทุกครั้ง เพื่อให้สามารถย้อนกลับมาดูได้

**อย่าใช้ test set จนกว่าจะถึงตอนสุดท้าย** - แบ่งเป็น train/validation/test แล้วใช้ validation สำหรับเลือกโมเดล เก็บ test set ไว้ประเมินผลครั้งเดียวก่อน deploy

## ตัวอย่างการใช้งาน

**ตัวอย่างที่ 1: User ส่ง CSV และอยากทำนายราคาบ้าน**

1. ถามประเภทปัญหา → regression
2. รัน EDA ด้วย `eda_template.py`
3. ใช้ `preprocessing_template.py` จัดการ missing values และ encode categorical
4. เริ่มด้วย Linear Regression เป็น baseline แล้วลอง Random Forest, Gradient Boosting
5. ประเมินด้วย RMSE และ R²

**ตัวอย่างที่ 2: User อยากทำ sentiment analysis**

1. ระบุว่าเป็น text classification
2. ใช้ TF-IDF หรือ embedding สำหรับ feature extraction
3. ลอง Logistic Regression เป็น baseline ก่อนข้ามไป transformer
4. ประเมินด้วย F1-score (เพราะมัก imbalance)

## PyCaret (AutoML multi-algorithm benchmark — ทางเลือกเสริม)

ใช้เมื่อผู้ใช้อยากเทียบหลายอัลกอริทึมพร้อมกันเร็วๆ (แทนการเขียน sklearn ทีละโมเดล) โดยเฉพาะงาน **anomaly detection** ที่ label ฝั่ง minority class มีน้อยเกินจะทำ supervised classification (ดูตัวอย่างจริงที่ทำมาแล้วใน [[pycaret-anomaly-comparison-2026-08-04]] — miss-judgment XPort LED)

### ⚠️ ต้องแยก environment เสมอ — ห้ามลงใน base env

เครื่องนี้ (miniconda base) มักมี Python เวอร์ชันใหม่กว่าที่ PyCaret รองรับมาก (พบแล้ว: base = Python 3.14 + pandas 3.x/sklearn 1.9) แต่ **PyCaret 3.3.2 pin เวอร์ชันเก่ากว่ามาก** (`numpy<1.27`, `pandas<2.2.0`, `scipy<=1.11.4`) — ลงรวมกับ base env จะพัง package เดิมที่ project อื่นใช้อยู่ ต้องสร้าง conda env แยกทุกครั้ง:

```bash
# ต้องใช้ --override-channels -c conda-forge เสมอ — ถ้าไม่ใส่ --override-channels
# conda จะดึง default channel (repo.anaconda.com) มาด้วยและ error เรื่อง
# "Terms of Service have not been accepted" (เครื่องนี้ไม่เคย accept ToS ไว้
# และไม่ควร accept แทนผู้ใช้เองโดยไม่ถาม — legal agreement)
conda create -n <env_name> --override-channels -c conda-forge python=3.10 -y

# ถ้าเจอ ZstdError("Allocation error: not enough memory") กลางทาง —
# เครื่องนี้ RAM ว่างต่ำ (เคยเจอเหลือ ~2.3GB) ให้ conda clean --all -y
# แล้ว retry คำสั่งเดิมซ้ำ มักผ่านรอบสอง
conda run -n <env_name> pip install pycaret pandas openpyxl
conda run -n <env_name> python -c "from pycaret.anomaly import setup; print('ok')"
```

### รูปแบบการ benchmark (anomaly module)

ดึงรายชื่ออัลกอริทึมจาก `models().index` ของ PyCaret เอง อย่า hardcode list เอง (จะได้ list ที่ตรงกับเวอร์ชันที่ลงจริงเสมอ) — ดู `assets/pycaret_anomaly_template.py`

**Gotcha ที่เจอแล้วจริง:** algorithm `sod` (จาก `pyod`) crash ด้วย `KeyError` เมื่อ `predict_model()` รับ pandas DataFrame ตรงๆ (bug ของ pyod เอง ไม่ใช่ของเรา) — ต้อง wrap **ทั้ง** `create_model()` และ `predict_model()` ในลูปเดียวกันด้วย `try/except` ต่ออัลกอริทึม ไม่ใช่แค่ `create_model()` เฉยๆ ไม่งั้นทั้ง run จะตายกลางทางและเสียผลลัพธ์ที่คำนวณไปแล้วก่อนหน้า

### ข้อจำกัดเรื่อง report/plot ในตัว

`pycaret.anomaly` เป็น unsupervised module — `plot_model()` รองรับแค่ `'tsne'`/`'umap'` เท่านั้น **ไม่มี** ROC curve / confusion matrix / feature importance ให้ในตัว (ต่างจาก `pycaret.classification`/`regression` ที่มีครบ) เพราะ module นี้ไม่ผูก label ไว้ตั้งแต่ `setup()`

ถ้าต้องการ ROC/confusion matrix จริงๆ และมี label ที่รู้ผลอยู่แล้ว (เอาไว้ประเมินหลังเทรนเท่านั้น ไม่ใช่เทรน) ให้ดึง `Anomaly_Score`/`Anomaly` column จาก `predict_model()` มาคำนวณเองด้วย sklearn (`roc_curve`, `confusion_matrix`) แล้วส่งต่อให้ [[ml-report]] จัดการ plot — **อย่า** เปลี่ยนไปใช้ `pycaret.classification` เพียงเพราะอยากได้ dashboard/ROC สำเร็จรูป ถ้า minority class มี n น้อยและไม่มี unit/piece ID ให้ group-split (จะเจอ data leakage เหมือนที่เคยเกิดในรายงาน XPort LED ฉบับแรกที่ต้องแก้ไขทีหลัง) — เช็คให้แน่ใจว่า group-aware split ทำได้จริงก่อนเปลี่ยน module

`dashboard()` (Explainer Dashboard) และ `create_app()` (Gradio demo) ก็เป็นของ `classification`/`regression` module เท่านั้นเช่นกัน มีข้อจำกัดเดียวกัน

## หมายเหตุ

หากผู้ใช้ต้องการแค่ explore ข้อมูลโดยไม่ทำ ML ใช้ skill นี้ในส่วน EDA ได้เลย ไม่จำเป็นต้องไปจนถึงขั้น training
