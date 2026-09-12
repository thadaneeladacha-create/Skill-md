# setup-matt-pocock-skills — วิธีติดตั้งและปัญหาที่เจอ

Scaffold per-repo config ที่ engineering skills ชุด Matt Pocock (`to-tickets`, `triage`, `to-spec`, `dev-pipeline`)
ใช้อ้างอิง: issue tracker อยู่ที่ไหน, triage label ใช้ชื่ออะไร, domain docs (`CONTEXT.md`/ADR) อยู่ที่ไหน
เป็น skill แบบ prompt-driven (สำรวจ repo → เสนอค่า → ถาม user ทีละ section → เขียนไฟล์) ไม่ใช่ script อัตโนมัติ

## วิธีติดตั้งบนเครื่องใหม่

1. Copy ทั้งโฟลเดอร์นี้ (`SKILL.md` + `domain.md` + `issue-tracker-*.md` + `triage-labels.md` + `agents/`)
   ไปที่ `~/.claude/skills/setup-matt-pocock-skills/`
   - Windows: `C:\Users\<user>\.claude\skills\setup-matt-pocock-skills\`
   - Mac/Linux: `~/.claude/skills/setup-matt-pocock-skills/`
2. เปิด Claude Code session ใหม่
3. ในแต่ละ repo ที่ต้องการใช้: รัน `/setup-matt-pocock-skills`

## Optional dependency

- ถ้าต้องการ label triage เต็มรูปแบบ (Section B ของ skill) ต้องติดตั้ง skill ชื่อ `triage` ไว้ด้วย —
  ถ้าไม่มี skill นี้ Section B จะถูกข้ามอัตโนมัติ ไม่ error
- ถ้าเลือก issue tracker เป็น **GitHub** ต้องมี [`gh` CLI](https://cli.github.com/) ติดตั้งและ `gh auth login`
  แล้วบนเครื่องนั้น — ถ้าเลือก **GitLab** ต้องมี [`glab` CLI](https://gitlab.com/gitlab-org/cli) แทน
  ถ้าเลือก **local markdown** (default เมื่อ repo ไม่มี git remote) ไม่ต้องติดตั้งอะไรเพิ่ม

## ปัญหา/ข้อจำกัดที่เจอจริง

- **`gh` CLI ไม่ได้ติดตั้งมาโดย default บน Windows** — ทดสอบจริงแล้วพบว่า `gh` ใช้ไม่ได้ทั้งใน Git Bash และ
  PowerShell บนเครื่องที่ไม่ได้ติดตั้งไว้ก่อน (`command not found` / `not recognized`) ถ้าจะเลือก issue tracker
  เป็น GitHub ต้องติดตั้ง CLI นี้เองก่อน ไม่งั้น `to-tickets`/`to-spec` ที่พึ่งพา `gh issue create` จะใช้งานไม่ได้
- **ต้องเลือกไฟล์ CLAUDE.md หรือ AGENTS.md เองถ้ายังไม่มีทั้งคู่** — skill นี้จะไม่เดาให้ ถ้า repo ไม่มีทั้ง
  `CLAUDE.md` และ `AGENTS.md` อยู่แล้ว มันจะหยุดถามผู้ใช้ก่อนเสมอ (ห้ามสร้างทั้งสองไฟล์พร้อมกัน)
- **repo ที่ไม่มี git remote เลย** (เช่น local research repo ไม่ได้ push ขึ้น GitHub/GitLab) จะ default ไปที่
  local-markdown tracker (`.scratch/<feature>/`) โดยอัตโนมัติ — ต้องระวังตอนตอบคำถาม Section A ถ้าตั้งใจจะใช้
  GitHub จริงๆ ในอนาคต ให้เลือก "Other" หรือเปลี่ยนคำตอบเป็น GitHub ด้วยมือแทนค่า default
- **การ setup ไม่กระทบโค้ด/feature อื่นในโปรเจกต์เลย** — ผลลัพธ์มีแค่ไฟล์ config ใหม่ 3 ไฟล์
  (`docs/agents/issue-tracker.md`, `docs/agents/domain.md`, `docs/agents/triage-labels.md` — ตัวหลังนี้เขียน
  เฉพาะเมื่อ `triage` ติดตั้งอยู่) และ section `## Agent skills` ที่เพิ่ม/แก้ในไฟล์ CLAUDE.md/AGENTS.md ที่มีอยู่
  แบบ in-place (ไม่ทับ section อื่นที่ user เขียนไว้เอง)
- **ต้องรันก่อน `/dev-pipeline` เสมอ** — `/dev-pipeline` มี pre-flight check ที่บล็อกไม่ให้เข้า `to-spec` ถ้า
  repo ยังไม่เคยรัน skill นี้มาก่อน (เช็คจาก `## Agent skills` block ใน CLAUDE.md/AGENTS.md)
- **Re-run skill นี้จำเป็นเฉพาะตอนต้องการเปลี่ยน issue tracker หรือ reset ใหม่ทั้งหมด** — ไม่งั้นแก้
  `docs/agents/*.md` ตรงๆ ได้เลยโดยไม่ต้องรัน skill ซ้ำ
