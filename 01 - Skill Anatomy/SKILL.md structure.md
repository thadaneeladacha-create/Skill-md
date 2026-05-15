---
tags:
  - skill/anatomy
title: SKILL.md structure
created: 2026-05-13
---

# SKILL.md structure

## โครงสร้างไฟล์โดยรวม

```
skill-name/
├── SKILL.md (จำเป็น)
│   ├── YAML frontmatter (name, description)
│   └── เนื้อหา markdown
└── Bundled Resources (ไม่บังคับ)
    ├── scripts/      — โค้ดอัตโนมัติ
    ├── references/   — เอกสารอ้างอิง
    └── assets/       — template, icon, font
```

## ส่วนประกอบของ SKILL.md

### 1. Frontmatter (บังคับ)

```yaml
---
name: skill-name
description: ใช้เมื่อไหร่ และทำอะไร
---
```

ดูรายละเอียดที่ [[YAML frontmatter]] และ [[Description writing]]

### 2. หัวข้อ / Overview

อธิบายสั้น ๆ ว่า skill นี้ทำอะไร

### 3. Workflow / ขั้นตอน

บอก Claude เป็นลำดับว่าต้องทำอะไรก่อนหลัง

### 4. References

ชี้ไปยังไฟล์ใน `references/` หรือ `assets/` ที่จำเป็น

### 5. ตัวอย่างการใช้งาน

ช่วย Claude เข้าใจรูปแบบ input/output

## หลักการสำคัญ

- **ความยาว**: ไม่เกิน ~500 บรรทัด — ถ้าเกินให้ split ไป references/
- **ใช้ภาษาคำสั่ง (imperative)** ในการเขียน
- **อธิบาย why** ไม่ใช่แค่ what
- ดูเพิ่มที่ [[Progressive disclosure]]

## ไปต่อที่

- [[YAML frontmatter]]
- [[Bundled resources]]
- [[Writing style]]
