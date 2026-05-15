---
tags:
  - skill/best-practice
title: Progressive disclosure
created: 2026-05-13
---

# Progressive disclosure

> หลักการ "เปิดเผยข้อมูลทีละชั้น" — Claude โหลดเฉพาะที่จำเป็น ประหยัด context

## 3 ระดับการโหลด

### Level 1 — Metadata (อยู่ใน context ตลอด)

- `name` + `description` ใน frontmatter
- ขนาด ~100 คำ
- ทุก skill จะมีส่วนนี้อยู่ในความรู้ของ Claude

### Level 2 — SKILL.md body (โหลดเมื่อ trigger)

- เนื้อหาทั้งหมดของ SKILL.md
- ควรไม่เกิน **500 บรรทัด**
- โหลดเข้า context ทันทีที่ skill ถูกเรียก

### Level 3 — Bundled resources (โหลดตามต้องการ)

- `references/*.md` — Claude อ่านเฉพาะที่ต้องการ
- `scripts/*` — รันได้โดยไม่ต้องอ่าน
- `assets/*` — copy ไปใช้

## ทำไมสำคัญ

- ✅ ประหยัด context window
- ✅ Skill ใหญ่ขึ้นได้โดยไม่ทำให้ทุกการเรียกช้า
- ✅ Multi-domain skill ใช้งานง่าย

## ตัวอย่างการจัด structure

```
cloud-deploy/
├── SKILL.md              ← workflow ทั่วไป + เลือก provider
└── references/
    ├── aws.md            ← เปิดเฉพาะถ้าใช้ AWS
    ├── gcp.md            ← เปิดเฉพาะถ้าใช้ GCP
    └── azure.md          ← เปิดเฉพาะถ้าใช้ Azure
```

ใน SKILL.md:
```markdown
ถ้า user ใช้ AWS → อ่าน `references/aws.md`
ถ้า user ใช้ GCP → อ่าน `references/gcp.md`
```

## Anti-pattern

❌ ใส่ทุกอย่างใน SKILL.md จนยาว 2,000 บรรทัด
❌ บังคับ Claude อ่านทุก reference ทุกครั้ง

## ไปต่อที่

- [[Bundled resources]]
- [[SKILL.md structure]]
