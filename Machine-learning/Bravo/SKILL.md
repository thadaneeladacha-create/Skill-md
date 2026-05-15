---
name: machine-learning
description: ใช้ skill นี้ทุกครั้งที่ผู้ใช้ต้องการสร้าง ฝึก ประเมิน หรือ deploy โมเดล Machine Learning ครอบคลุมการเตรียมข้อมูล (data preprocessing), การเลือกอัลกอริทึม (classification, regression, clustering), การ train model ด้วย scikit-learn / PyTorch / TensorFlow, การประเมินผลด้วย metrics ต่าง ๆ (accuracy, F1, RMSE), การทำ hyperparameter tuning, cross-validation รวมถึงการแก้ปัญหา overfitting/underfitting และการสร้าง pipeline สำหรับ ML. ให้ trigger ทันทีเมื่อผู้ใช้พูดถึง "โมเดล", "เทรนโมเดล", "ML", "AI", "predict", "classification", "regression", "neural network", "deep learning", "sklearn", "pandas สำหรับ ML", หรือเมื่ออัพโหลด dataset (.csv, .parquet) แล้วถามว่าจะวิเคราะห์/พยากรณ์ยังไง แม้ไม่ได้พูดคำว่า "machine learning" ตรง ๆ ก็ตาม
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

## หมายเหตุ

หากผู้ใช้ต้องการแค่ explore ข้อมูลโดยไม่ทำ ML ใช้ skill นี้ในส่วน EDA ได้เลย ไม่จำเป็นต้องไปจนถึงขั้น training
