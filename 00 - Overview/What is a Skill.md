---
tags:
  - skill/overview
title: What is a Skill
created: 2026-05-13
---

# What is a Skill

> Skill คือชุดคำสั่งและทรัพยากรที่ถูกบรรจุไว้เป็นโฟลเดอร์ เพื่อให้ Claude เรียกใช้เมื่อเจองานเฉพาะทาง

## นิยาม

**Skill** = โฟลเดอร์ที่ประกอบด้วย `SKILL.md` (ไฟล์หลัก) และ resource เพิ่มเติม (`scripts/`, `references/`, `assets/`) — ทำหน้าที่เหมือน "playbook" สำหรับ Claude

## ทำไมต้องใช้ Skill

- **Reusable** — เขียนครั้งเดียว ใช้ได้ทุกครั้งที่ตรง trigger
- **Domain knowledge** — เก็บความรู้เฉพาะทางไว้ที่เดียว
- **Progressive disclosure** — โหลดข้อมูลเฉพาะที่จำเป็น ประหยัด context
- **Quality control** — บังคับให้ Claude ทำตามขั้นตอนที่ผ่านการ test แล้ว

## องค์ประกอบหลัก

```
my-skill/
├── SKILL.md              ← จุดเริ่มต้น (จำเป็น)
├── scripts/              ← โค้ดอัตโนมัติ
├── references/           ← เอกสารอ้างอิง
└── assets/               ← template, fonts, icons
```

ดูรายละเอียดที่ [[SKILL.md structure]]

## ตัวอย่าง skill ที่เห็นบ่อย

- `pdf` — จัดการ PDF (extract, merge, fill form)
- `xlsx` — สร้างและแก้ไข Excel
- `pptx` — สร้าง slide deck
- `skill-creator` — meta-skill สำหรับสร้าง skill อื่น ๆ

## ไปต่อที่

- [[When to create a Skill]]
- [[SKILL.md structure]]
