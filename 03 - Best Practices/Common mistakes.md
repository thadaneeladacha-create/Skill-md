---
tags:
  - skill/best-practice
title: Common mistakes
created: 2026-05-13
---

# Common Mistakes

> รวมข้อผิดพลาดที่พบบ่อยและวิธีหลีกเลี่ยง

## ❌ Description อ่อนเกินไป

```yaml
description: ทำเอกสาร
```

→ Claude ไม่รู้ว่าควรเรียกเมื่อไหร่

**แก้ด้วย**: [[Description writing]]

## ❌ SKILL.md ยาวเกินไป

มากกว่า 500 บรรทัด → หาส่วนที่เป็น reference แล้วย้ายไป `references/`

**แก้ด้วย**: [[Progressive disclosure]]

## ❌ ใส่ "When to use" ในเนื้อหา ไม่ใส่ใน description

Claude ตัดสิน trigger จาก description เท่านั้น

## ❌ ใช้ ALWAYS / NEVER เยอะเกิน

แทนที่ด้วยการอธิบาย why

**แก้ด้วย**: [[Writing style]]

## ❌ Overfit test cases

เขียน skill ที่ทำงานเฉพาะกับ test ที่ใช้ — เมื่อใช้จริงพัง

**แก้ด้วย**: คิดเป็น "rule" ทั่วไป ไม่ใช่ "fix" เฉพาะ case

## ❌ ไม่มี baseline เปรียบเทียบ

รันแค่ with_skill — ไม่รู้ว่า skill ทำให้ดีขึ้นจริงมั้ย

**แก้ด้วย**: รัน without_skill คู่ตลอด

## ❌ Test case ไม่ realistic

ใช้ prompt สั้น ๆ ไม่มีบริบท — ไม่สะท้อนการใช้งานจริง

**แก้ด้วย**: คิดเป็น "user จริงพิมพ์อะไร" — มี backstory, ชื่อไฟล์, รายละเอียด

## ❌ ใส่ assertion ที่ผ่านง่ายเกินไป

```python
assert output is not None  # ผ่านได้ทุกครั้งโดยไม่บอกอะไร
```

**แก้ด้วย**: assertion ที่ specific และ verify quality

## ❌ ไม่ iterate

draft แรกแล้วใช้เลย — ไม่ได้ดูว่าดีจริงมั้ย

**แก้ด้วย**: ทำตาม [[5. Iteration loop]]

## ไปต่อที่

- [[_MOC|กลับ MOC]]
