---
tags:
  - skill/best-practice
title: Examples and Patterns
created: 2026-05-13
---

# Examples and Patterns

> Pattern ที่ใช้ซ้ำได้ในการเขียน SKILL.md

## Pattern 1: Output format template

ระบุ output format ให้ชัดด้วย template:

```markdown
## Report structure
ใช้ template นี้:

# [Title]
## Executive Summary
## Key Findings
## Recommendations
```

## Pattern 2: Examples (Input → Output)

```markdown
## Commit message format

**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication

**Example 2:**
Input: Fixed bug in payment processing
Output: fix(payment): resolve checkout flow error
```

## Pattern 3: Decision tree

```markdown
## เลือกโมเดล

- ถ้า target เป็นตัวเลขต่อเนื่อง → ใช้ regression
  - มี features < 1000 → Linear/Ridge
  - features เยอะ + non-linear → Random Forest
- ถ้า target เป็น class → ใช้ classification
  - 2 class → Logistic Regression baseline
  - หลาย class + imbalance → ใช้ F1
```

## Pattern 4: Step-by-step workflow

```markdown
## Workflow

1. โหลดข้อมูล
2. EDA — สำรวจ
3. Preprocess
4. Train
5. Evaluate
6. Deploy
```

## Pattern 5: Reference loading

```markdown
## เลือก provider

- ถ้า user ใช้ AWS → อ่าน `references/aws.md`
- ถ้า user ใช้ GCP → อ่าน `references/gcp.md`

ไม่ต้องโหลดทั้งหมด — เลือกเฉพาะที่ตรง
```

## Pattern 6: Bundled script invocation

```markdown
## สร้าง report

รันคำสั่งนี้ — ไม่ต้องเขียน script เอง:

`python scripts/generate_report.py --input <path>`
```

## ไปต่อที่

- [[Writing style]]
- [[Progressive disclosure]]
