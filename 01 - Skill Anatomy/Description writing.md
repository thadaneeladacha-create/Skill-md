---
tags:
  - skill/anatomy
  - skill/best-practice
title: Description writing
created: 2026-05-13
---

# Description writing

> Description คือ **ตัวตัดสิน** ว่า Claude จะเรียก skill หรือไม่ — ใส่ใจมากที่สุด

## สูตรการเขียน

```
[เมื่อไหร่ trigger]. [ทำอะไร]. [คำเฉพาะที่ user จะใช้].
[ตัวอย่าง use case]. [คำเตือนสำหรับการ undertrigger]
```

## ตัวอย่าง: ก่อน vs หลัง

### ❌ ก่อน (อ่อน)

```yaml
description: สร้าง dashboard แสดงข้อมูล
```

### ✅ หลัง (แข็งแรง)

```yaml
description: สร้าง dashboard เร็วและสวยสำหรับแสดงข้อมูลภายในบริษัท
  ให้ trigger ทุกครั้งที่ user พูดถึง dashboard, data visualization,
  internal metrics หรืออยากแสดงข้อมูลใด ๆ ของบริษัท แม้ไม่ได้
  พูดคำว่า "dashboard" ตรง ๆ ก็ตาม
```

## เทคนิคที่ใช้ได้ผล

### 1. ใส่ keyword หลายแบบ

ผู้ใช้พูดได้หลายแบบ — ใส่คำพ้องและคำที่ใช้บ่อย

```
PDF, .pdf, ไฟล์ PDF, เอกสาร PDF, pdf form, fill in PDF
```

### 2. ระบุ context ที่ trigger

```
เมื่อ user ส่งไฟล์ .csv แล้วถามว่าวิเคราะห์ยังไง
```

### 3. "pushy" บอก Claude ให้เรียกใช้

```
ให้ trigger ทันที แม้ไม่ได้พูดคำว่า "X" ตรง ๆ
```

### 4. ระบุ negative cases (กันเรียกผิด)

```
ห้าม trigger เมื่อพูดถึง spreadsheet หรือ Word doc
```

## ความยาว

- สั้นเกินไป (< 50 คำ) — Claude ไม่รู้ว่าควร trigger
- ยาวเกินไป (> 200 คำ) — เปลืองและสับสน
- จุดเหมาะ: ~80-150 คำ

## ทดสอบ description

หลังเขียนเสร็จ ลองคิดคำถาม 10 แบบที่ user น่าจะพิมพ์
- ครึ่งหนึ่ง "should trigger"
- อีกครึ่ง "should not trigger" (near-miss)

ถ้าคำถามที่ควร trigger ไม่ trigger → ปรับ description ให้กว้างขึ้น
ถ้า trigger ผิด → ปรับให้แคบลง

## ใช้เครื่องมือ optimize อัตโนมัติ

`skill-creator` มี script `run_loop.py` สำหรับ optimize description โดยอัตโนมัติ — ดูที่ [[6. Description optimization]]

## ไปต่อที่

- [[YAML frontmatter]]
- [[6. Description optimization]]
- [[Common mistakes]]
