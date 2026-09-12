# dev-pipeline — วิธีติดตั้งและปัญหาที่เจอ

Orchestrator ที่ร้อยลำดับ skill 6 ตัว (grill-with-docs → junior-to-senior → to-spec → to-tickets → implement → code-review)
ให้เป็น flow เดียวที่ทำซ้ำได้ทุกโปรเจกต์ ตัว `dev-pipeline` เองไม่ทำงานแทนตัวไหนเลย มันแค่เรียกแต่ละ skill
ผ่าน `Skill` tool ตามลำดับ พร้อม gate ก่อนข้ามขั้นที่ผลิต artifact ถาวร

## Dependency (ต้องติดตั้งก่อน)

`dev-pipeline` ไม่ทำงานลำพัง ต้องมี skill เหล่านี้อยู่ใน `~/.claude/skills/` ด้วย:

- `grill-with-docs` (เรียก `grilling` + `domain-modeling` ข้างใน)
- `junior-to-senior`
- `to-spec`
- `to-tickets`
- `implement` (เชน `tdd` → `code-review` → commit อยู่ในตัวแล้ว)
- `setup-matt-pocock-skills` (สำหรับ pre-flight check ก่อน `to-spec`)

ถ้าขาดตัวไหน pipeline จะพังตอนถึงสเตจนั้น

## วิธีติดตั้งบนเครื่องใหม่

1. Copy โฟลเดอร์นี้ (`dev-pipeline/SKILL.md`) ไปที่ `~/.claude/skills/dev-pipeline/SKILL.md`
   - Windows: `C:\Users\<user>\.claude\skills\dev-pipeline\SKILL.md`
   - Mac/Linux: `~/.claude/skills/dev-pipeline/SKILL.md`
2. ทำเช่นเดียวกันกับ skill dependency ทั้งหมดข้างบน (แต่ละ skill = 1 โฟลเดอร์ย่อยใต้ `~/.claude/skills/`)
3. เปิด Claude Code session ใหม่ (skill list โหลดตอนเริ่ม session)
4. ในแต่ละ repo ที่จะใช้ pipeล line: รัน `/setup-matt-pocock-skills` ก่อนอย่างน้อย 1 ครั้ง เพื่อสร้าง `docs/agents/*.md`
   + `## Agent skills` block ใน `CLAUDE.md`/`AGENTS.md` — ไม่งั้น pre-flight check จะบล็อกไม่ให้เข้า `to-spec`
5. เรียกใช้ผ่าน `/dev-pipeline <คำอธิบายฟีเจอร์>`

## ปัญหา/ข้อจำกัดที่เจอจริง (จากการทดสอบ end-to-end)

- **`grill-with-docs` และ `to-spec` เรียกผ่าน `Skill` tool อัตโนมัติไม่ได้** — ทั้งสองตัวมี `disable-model-invocation: true`
  ในตัวเอง เพราะงานเหล่านี้ควรถูก user เรียกเองโดยตรงเท่านั้น พอ `dev-pipeline` (หรือตัว pipeline agent) พยายามเรียกผ่าน
  `Skill({skill: "grill-with-docs"})` จะได้ error กลับมาทันที ("cannot be used with Skill tool due to
  disable-model-invocation") วิธีแก้: เมื่อ pipeline มาถึงสเตจนี้ ต้องบอกให้ user พิมพ์ `/grill-with-docs` หรือ
  `/to-spec` เองในข้อความถัดไป แล้ว agent ค่อยรับช่วง context ต่อ — **ห้าม** พยายาม replicate workflow ของ
  skill เหล่านี้ด้วยวิธีอื่นแทน (เช่น ทำ interview เองโดยไม่ผ่าน skill)
- **Pre-flight ก่อน `to-spec` เป็นเงื่อนไขบังคับ** — ถ้า repo ยังไม่เคยรัน `/setup-matt-pocock-skills` (ไม่มี
  `## Agent skills` block ใน `CLAUDE.md`/`AGENTS.md`) ต้องหยุดและบอกให้รันก่อน เพราะ `to-spec`/`to-tickets`
  ต้องใช้ tracker config + label vocabulary ที่ setup นั้นเขียนไว้
- **ไม่มี state file แยกเก็บ progress ของ pipeline เอง** — สถานะจริงอยู่ใน tracker (ticket status + blocking
  edges + label) หรือใน `.scratch/<feature-slug>/issues/*.md` ถ้าเป็น local tracker ตอน resume pipeline ใน
  session ใหม่ ต้องอ่านจากไฟล์เหล่านี้เพื่อดูว่าค้างอยู่ stage ไหน แทนการเดาจากบทสนทนาเก่า
- **Gate หลัง `junior-to-senior` สำคัญที่สุด** — ห้ามส่งต่อเข้า `to-spec` จนกว่า user จะตอบ open questions ที่
  `junior-to-senior` ทิ้งไว้ เพราะ `to-spec`/`to-tickets` publish เข้า tracker จริง แก้ย้อนหลังลำบากกว่าแก้ plan
  ในบทสนทนา
- **Implement ทีละ ticket ต่อ session เท่านั้น** — แม้ frontier (ticket ที่ blocker เสร็จครบแล้ว) จะมีมากกว่า
  1 ใบ ห้าม loop implement ต่อเนื่องข้าม ticket เองอัตโนมัติ ต้องให้ user เลือกทีละใบ
- **งานเล็กมาก (toy feature) ก็ยังต้องผ่านทุกสเตจ** — ทดสอบจริงกับ feature ระดับ "สร้างไฟล์ .txt 2 ไฟล์" แล้ว
  พบว่า pipeline ยังบังคับให้ผ่าน grill → review → spec → ticket ครบ แม้งานจะไม่มี ambiguity เลย ถ้าต้องการ
  ข้ามงานเล็กๆ ให้เรียก skill ย่อย (`/implement` ตรงๆ) หรือใช้ Plan Mode แทน ไม่ต้องผ่าน `/dev-pipeline`
  ทั้งชุด (ดู "เมื่อไหร่ควรใช้" ด้านล่าง)

## เมื่อไหร่ควรใช้ dev-pipeline vs Plan Mode

- **Plan Mode**: งานที่จบใน session เดียว ไม่ต้องมี artifact ถาวร (spec/ticket) — เบาและเร็ว
- **`/dev-pipeline`**: feature ใหญ่ที่ต้องแตกเป็นหลาย ticket ทำงานข้าม session ได้ (ticket publish ไว้ใน tracker
  ถาวร กลับมา resume ได้ทีหลัง) — คุ้มค่าเฉพาะตอนมี feature ใหญ่จริงๆ ไม่ใช่ default สำหรับทุกงาน
