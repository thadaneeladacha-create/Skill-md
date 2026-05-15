---
tags:
  - skill/anatomy
title: YAML frontmatter
created: 2026-05-13
---

# YAML frontmatter

> 2 บรรทัดบนสุดของ `SKILL.md` ที่กำหนดว่า skill นี้ชื่ออะไรและ trigger เมื่อไหร่

## รูปแบบ

```yaml
---
name: skill-name
description: คำอธิบายว่าใช้ตอนไหน + ทำอะไร
---
```

## Field ที่จำเป็น

### `name` (บังคับ)

- ใช้รูปแบบ kebab-case: `my-skill`, `pdf-extractor`
- ตรงกับชื่อโฟลเดอร์
- ไม่มีช่องว่าง ไม่มีอักขระพิเศษ

### `description` (บังคับ — สำคัญที่สุด)

- เป็น **กลไกหลัก** ที่ Claude ใช้ตัดสินว่าจะเรียก skill หรือไม่
- ต้องครอบคลุม:
  - **What** — skill ทำอะไร
  - **When** — trigger เมื่อไหร่ (ใส่คำเฉพาะที่ user จะพิมพ์)
- ควร "pushy" เล็กน้อย เพราะ Claude มักจะ "undertrigger"

ดูรายละเอียดที่ [[Description writing]]

## Field เสริม

### `compatibility` (ไม่ค่อยใช้)

ระบุ tool/dependency ที่ต้องใช้

```yaml
compatibility:
  tools: [Bash, Read]
  dependencies: [pandoc]
```

## ตัวอย่างที่ดี

```yaml
---
name: pdf
description: ใช้ทุกครั้งที่ผู้ใช้พูดถึง PDF, .pdf, extract, merge, split,
  form filling — รวมถึงเมื่อมีไฟล์ .pdf ในบทสนทนา และต้องการอ่าน/แก้ไข/สร้าง PDF
---
```

## ข้อผิดพลาดที่พบบ่อย

- ❌ description สั้นเกินไป — Claude ไม่รู้ว่าควร trigger ตอนไหน
- ❌ ใส่ "when to use" ในเนื้อหา ไม่ใส่ใน description
- ❌ ใช้ภาษากำกวม (เช่น "สำหรับงานเอกสาร")
- ❌ ลืม `---` คั่นทั้งบนและล่าง

## ไปต่อที่

- [[Description writing]]
- [[Common mistakes]]
