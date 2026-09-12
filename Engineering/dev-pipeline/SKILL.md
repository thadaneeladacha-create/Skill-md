---
name: dev-pipeline
description: End-to-end orchestrator that chains grill-with-docs → junior-to-senior → to-spec → to-tickets → implement into one repeatable feature workflow, with gates between stages. Trigger on "เริ่ม feature ใหม่", "วาง pipeline ให้ feature นี้", "ทำ feature นี้แบบ full flow", "/dev-pipeline", or when the user describes a new feature/idea from scratch and hasn't picked a single skill yet.
---

# Dev Pipeline

จัด**ลำดับงาน**ของ 6 skill ที่มีอยู่แล้ว (grill-with-docs, junior-to-senior, to-spec, to-tickets, implement, code-review)
ให้เป็น flow เดียวที่ทำซ้ำได้ทุกโปรเจค — skill นี้**ไม่แทนที่**ตัวไหนเลย มันแค่เรียกแต่ละตัวผ่าน `Skill` tool
ตามลำดับ พร้อม gate ให้ผู้ใช้ยืนยันก่อนข้ามขั้นที่ผลิต artifact ถาวร (spec/ticket ที่ publish เข้า tracker)

ผู้ใช้ยังเรียก skill ย่อยตรงๆ ได้เสมอ (`/to-spec`, `/implement`, ...) โดยไม่ต้องผ่าน pipeline นี้เลยก็ได้

## State machine

```
[ไอเดีย/plan ดิบในบทสนทนา]
        │
        ▼
   grill-with-docs (/grilling + /domain-modeling)
        │  → plan ที่ถูกซักไซ้แล้ว + CONTEXT.md/ADR อัปเดต
        ▼
   junior-to-senior
        │  → Promoted Plan v2 (blocker/major/minor findings + open questions)
        │     [GATE] ผู้ใช้ตอบ open questions / ยืนยันแผน v2 ก่อนไปต่อ
        ▼
   [PRE-FLIGHT] เช็คว่า repo นี้รัน /setup-matt-pocock-skills แล้วหรือยัง
        │  (มองหา "## Agent skills" block ใน CLAUDE.md หรือ AGENTS.md)
        ├─ ยังไม่มี → บอกผู้ใช้ให้รัน /setup-matt-pocock-skills ก่อน แล้วหยุดรอ
        └─ มีแล้ว → ไปต่อ
        ▼
   to-spec  (รับ Promoted Plan v2 เป็น input)
        │  → spec doc publish เข้า tracker พร้อม label ready-for-agent
        ▼
   to-tickets  (รับ spec จากขั้นก่อนเป็น input)
        │  → tracer-bullet tickets + blocking edges, publish เข้า tracker
        │     [GATE] to-tickets เอง quiz ผู้ใช้เรื่อง granularity/blocking edges อยู่แล้ว — ไม่ต้องเพิ่มซ้อน
        ▼
   ── จบ session นี้ ── ต่อ session ถัดไป (ทำซ้ำได้เรื่อยๆ จนกว่า ticket จะหมด) ──
        ▼
   implement <ticket ถัดไปที่เป็น frontier>
        │  → tdd → code-review → commit (เชนอยู่ภายใน implement เองแล้ว)
        └─ ยังมี ticket เหลือ → กลับไปเริ่ม implement รอบใหม่ใน session ถัดไป
```

## Dispatch table

| Stage | เรียกอะไร | Input | Output ที่ต้องส่งต่อ stage ถัดไป |
|---|---|---|---|
| 1. Grill | `Skill({skill: "grill-with-docs"})` | ไอเดีย/พล็อตดิบจากผู้ใช้ในบทสนทนา | plan ที่ผ่านการซักไซ้ + doc ที่อัปเดต |
| 2. Review | `Skill({skill: "junior-to-senior"})` | plan จาก stage 1 | Promoted Plan v2 + open questions ที่ต้องให้ผู้ใช้ตอบ |
| 3. Spec | `Skill({skill: "to-spec"})` | Promoted Plan v2 (หลังผู้ใช้ตอบ open questions) | spec doc ที่ publish แล้ว (พร้อม id/URL บน tracker) |
| 4. Tickets | `Skill({skill: "to-tickets", args: "<spec ref>"})` | spec doc/ref จาก stage 3 | ticket list พร้อม blocking edges ที่ publish แล้ว |
| 5. Implement | `Skill({skill: "implement", args: "<ticket ref>"})` | หนึ่ง ticket ที่เป็น frontier (blocker เสร็จหมดแล้ว) | โค้ดที่ commit แล้ว |

## กติกาสำคัญ

- **Implement ทีละใบ ต่อ session** — เมื่อมาถึง stage 5 ให้บอกผู้ใช้ว่า ticket ไหนคือ frontier ตอนนี้ (blocker
  เสร็จครบแล้ว) แล้วให้ผู้ใช้เลือกว่าจะ implement ใบไหนใน session นี้ **ห้าม loop implement ต่อเนื่องข้าม
  ticket เองอัตโนมัติ** แม้ frontier จะมีมากกว่า 1 ใบก็ตาม
- **ไม่มี state file แยก** — สถานะจริงอยู่ใน tracker เอง (ticket status + blocking edges + label) หรือใน
  `.scratch/<feature-slug>/issues/*.md` ถ้าเป็น local tracker ตอน resume pipeline ใน session ใหม่ ให้อ่านจาก
  tracker/ไฟล์เหล่านี้เพื่อดูว่าค้างอยู่ stage ไหน/ticket ไหนเป็น frontier แทนการเดา
- **Gate หลัง junior-to-senior คือจุดหยุดที่สำคัญที่สุด** — ห้ามส่งต่อเข้า to-spec จนกว่าผู้ใช้จะตอบ open
  questions ที่ junior-to-senior ทิ้งไว้ (ใช้ `AskUserQuestion` ถ้าจำเป็น) เพราะ to-spec/to-tickets publish
  เข้า tracker จริง แก้ย้อนหลังลำบากกว่าแก้ plan ในบทสนทนา
- **Pre-flight ก่อน to-spec เป็นเงื่อนไขบังคับ** — อย่าเรียก `/to-spec` หรือ `/to-tickets` ถ้า repo ยังไม่เคยรัน
  `/setup-matt-pocock-skills` เพราะทั้งสอง skill ต้องใช้ tracker config + label vocabulary ที่ setup นั้นเขียนไว้
- **code-review ไม่ต้องเรียกแยก** — มันถูกเชนอยู่ภายใน `implement` (tdd → code-review → commit) อยู่แล้ว
