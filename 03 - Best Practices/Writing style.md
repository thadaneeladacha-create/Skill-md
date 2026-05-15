---
tags:
  - skill/best-practice
title: Writing style
created: 2026-05-13
---

# Writing style

> เขียน skill เหมือนอธิบายให้เพื่อนเก่งที่เพิ่งเข้ามาทำงานใหม่ฟัง

## หลัก 4 ข้อ

### 1. ใช้ imperative form

```markdown
❌ "ผู้ใช้ควรตรวจสอบ missing value"
✅ "ตรวจสอบ missing value ก่อน fit model"
```

### 2. อธิบาย why ไม่ใช่แค่ what

LLM ยุคนี้ฉลาด — ถ้าเข้าใจ why จะรับมือกับ edge cases ได้เอง

```markdown
❌ "ALWAYS ใส่ random_state=42"

✅ "ใส่ random_state=42 เพื่อให้ผลลัพธ์ reproducible —
   ผู้ใช้รันซ้ำได้ผลเหมือนเดิม"
```

### 3. หลีกเลี่ยง ALWAYS / NEVER ตัวใหญ่

ถ้าเจอตัวเองเขียน ALWAYS — สัญญาณว่าควรอธิบายเหตุผลแทน

### 4. ทำให้ general ไม่ overfit

อย่าเขียนเฉพาะ test case — ออกแบบให้รองรับ scenario หลากหลาย

## สไตล์ที่ดี

- หัวข้อชัด ใช้ heading
- โค้ดตัวอย่างประกอบ
- ข้อความสั้น กระชับ
- เน้นเฉพาะคำสำคัญด้วย **bold**

## ไม่ใช้

- ❌ Emoji เกินจำเป็น
- ❌ ภาษาตลาด ไม่เป็นทางการเกินไป
- ❌ คำที่ทำให้สับสน

## ไปต่อที่

- [[3. Write SKILL.md]]
- [[Examples and Patterns]]
