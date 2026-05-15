---
tags:
  - skill/template
title: Test Case Template
created: 2026-05-13
---

# Test Case — {{ Eval Name }}

## Prompt

```
{{ ใส่ prompt ที่ user น่าจะพิมพ์จริง ๆ — มี context, ชื่อไฟล์, ตัวเลข }}
```

## Expected output

- อธิบายว่าควรได้อะไร
- รูปแบบไฟล์ output
- คุณสมบัติที่ต้องมี

## Files / Input

- `sample_input.csv`
- ...

## Assertions (Quantitative)

```json
[
  {
    "text": "output มี header 'Summary'",
    "type": "contains",
    "value": "Summary"
  },
  {
    "text": "ไฟล์ output มี extension .pdf",
    "type": "file_extension",
    "value": ".pdf"
  }
]
```

## Qualitative review

จุดที่ต้องดูเอง:
- [ ] format ดูดีไหม
- [ ] เนื้อหาครบ
- [ ] โทนเหมาะกับงาน

## Results

| Iteration | With Skill | Without Skill | Note |
| --------- | ---------- | ------------- | ---- |
| 1         |            |               |      |
| 2         |            |               |      |

## Feedback

(บันทึก feedback จากผู้ใช้)

## Related

- [[4. Test cases and Evaluation]]
