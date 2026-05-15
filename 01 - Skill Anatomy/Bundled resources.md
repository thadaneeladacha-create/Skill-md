---
tags:
  - skill/anatomy
title: Bundled resources
created: 2026-05-13
---

# Bundled resources

> ไฟล์เสริมที่อยู่ในโฟลเดอร์ skill — โหลดเฉพาะเมื่อจำเป็น (ดู [[Progressive disclosure]])

## โฟลเดอร์ย่อยมาตรฐาน

### 📁 `scripts/`

> โค้ดสำหรับงานซ้ำซ้อนหรือ deterministic

- Python script, Bash script
- Claude **รัน** script (ไม่ต้องอ่านโค้ดเข้า context)
- ตัวอย่าง: `convert_pdf.py`, `aggregate_benchmark.py`

```python
# scripts/example.py
def process(input_path):
    ...
```

ใน SKILL.md ระบุว่า:
```markdown
รัน `python scripts/example.py <input>` เพื่อ...
```

### 📁 `references/`

> เอกสารอ้างอิงที่ Claude อ่านเฉพาะตอนที่ใช้

- Markdown file
- เหมาะกับข้อมูลที่ยาว, technical details, schemas
- ตัวอย่าง: `references/schemas.md`, `references/aws.md`

```markdown
ดูรายละเอียดที่ `references/aws.md` ถ้า user ใช้ AWS
```

### 📁 `assets/`

> ไฟล์ที่ใช้ในผลลัพธ์ (templates, fonts, icons)

- ไม่ถูกอ่านเข้า context แต่ถูก copy ไปใช้
- ตัวอย่าง: template `.docx`, font files, image assets

## เลือกใช้ folder ไหน?

| ประเภท | folder |
|---|---|
| โค้ดที่รัน | `scripts/` |
| ข้อมูลที่อ่าน | `references/` |
| ไฟล์ที่ copy ไปใช้ | `assets/` |

## เคล็ดลับ

- **อย่าใส่ทุกอย่างใน SKILL.md** — แตกออกมาเป็น references/ ถ้ายาว
- **Domain organization** — ถ้า skill รองรับหลาย variant ให้แยกเป็นไฟล์
  ```
  references/aws.md
  references/gcp.md
  references/azure.md
  ```
- **สำหรับ reference ยาว (>300 บรรทัด)** — ใส่ table of contents ที่ต้น

## ไปต่อที่

- [[Progressive disclosure]]
- [[SKILL.md structure]]
