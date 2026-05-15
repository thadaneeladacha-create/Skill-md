---
tags:
  - skill/case-study
title: "Case Study: Machine Learning Skill"
created: 2026-05-13
---

# 🧪 Case Study — Machine Learning Skill

> ตัวอย่าง skill จริงที่สร้างตามหลักการใน vault นี้ — อ่านควบคู่กับ note อื่น ๆ เพื่อเห็นภาพการประยุกต์

## 📌 Skill นี้คืออะไร

**Skill name:** `machine-learning`

**ตำแหน่ง:** `Skills/machine-learning/`

**หน้าที่:** ช่วย Claude ทำงาน Machine Learning ตั้งแต่ EDA, preprocessing, training, evaluation, hyperparameter tuning

## 🗂️ โครงสร้างจริง

```
machine-learning/
├── SKILL.md
└── assets/
    ├── requirements.txt
    ├── eda_template.py
    ├── preprocessing_template.py
    ├── model_classification_template.py
    ├── model_regression_template.py
    ├── model_neural_network_template.py
    ├── evaluation_template.py
    └── hyperparameter_tuning_template.py
```

## 🎯 ตามหลักการใน vault อย่างไร

### Frontmatter / Description

ดู [[YAML frontmatter]] และ [[Description writing]]

```yaml
name: machine-learning
description: ใช้ skill นี้ทุกครั้งที่ผู้ใช้ต้องการสร้าง ฝึก ประเมิน หรือ deploy
  โมเดล Machine Learning ครอบคลุม...
  ให้ trigger ทันทีเมื่อผู้ใช้พูดถึง "โมเดล", "เทรนโมเดล", "ML", ...
```

ทำตามสูตรของ [[Description writing]]:

- ✅ "เมื่อไหร่ trigger" — ทุกครั้งที่ผู้ใช้ทำ ML
- ✅ คำเฉพาะ — ใส่ทั้งภาษาไทย/อังกฤษ (โมเดล, ML, classification, regression, sklearn)
- ✅ "pushy" — บอกว่าให้ trigger แม้ไม่พูดคำตรง

### Progressive Disclosure

ดู [[Progressive disclosure]]

- **Level 1 (metadata):** frontmatter อยู่ใน context ตลอด
- **Level 2 (SKILL.md):** workflow + best practices ที่ Claude ต้องรู้
- **Level 3 (assets/):** template Python — Claude อ่านเฉพาะตอนใช้งาน ไม่ต้องโหลดเข้า context

→ ใช้ asset แทน script เพราะ template เป็น "code ให้ copy ไปปรับ" ไม่ใช่ "code ที่รันทันที"

### Bundled Resources

ดู [[Bundled resources]]

ใช้แค่ `assets/` ไม่มี `scripts/` หรือ `references/` เพราะ:

- ไม่มี script deterministic ที่รันซ้ำ ๆ ได้ → ไม่ใช้ scripts/
- workflow ทั้งหมดอยู่ใน SKILL.md ได้ใน 500 บรรทัด → ไม่ต้อง references/
- มี template หลายไฟล์ที่ Claude เรียกใช้ตามบริบท → assets/

### Writing Style

ดู [[Writing style]]

- ใช้ imperative form ("ตรวจสอบ missing values", "เริ่มจาก baseline")
- อธิบาย why ("ใช้ random_state=42 เพื่อให้ reproducible")
- ไม่มี ALWAYS/NEVER ตัวใหญ่

### Workflow ของ skill

ตาม [[3. Write SKILL.md]] — มี section ตามลำดับ:

1. ทำความเข้าใจโจทย์
2. EDA
3. Preprocessing
4. Training
5. Evaluation
6. Hyperparameter Tuning
7. ตรวจสอบ Overfitting

## 🔍 ส่วนที่ยังขาด (ถ้าจะทำต่อ)

- [ ] `evals/evals.json` — test cases (ดู [[4. Test cases and Evaluation]])
- [ ] รัน optimization loop (ดู [[6. Description optimization]])
- [ ] เพิ่ม `references/` แยกตาม domain (NLP, computer vision, time-series)

## 📂 ไฟล์ที่เกี่ยวข้อง

- [SKILL.md หลัก](Skills/machine-learning/SKILL.md)
- [requirements.txt](Skills/machine-learning/assets/requirements.txt)
- [EDA template](Skills/machine-learning/assets/eda_template.py)

## 🔗 Related Notes

- [[_MOC]]
- [[SKILL.md structure]]
- [[Examples and Patterns]]
- [[Common mistakes]]
