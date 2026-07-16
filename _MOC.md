---
tags:
  - MOC
  - index
title: Map of Content - How to Build a Claude Skill
created: 2026-05-13
---

# 🗺️ Map of Content — How to Build a Claude Skill

> Vault สำหรับรวบรวมความรู้และแนวทางการสร้าง Claude Skill ตั้งแต่เริ่มต้นจนถึงการ optimize

---

## 📂 โครงสร้าง Vault

### 00 — Overview (พื้นฐาน)

- [[What is a Skill]] — Skill คืออะไรและทำหน้าที่อะไร
- [[When to create a Skill]] — ตัดสินใจว่าเมื่อไหร่ควรสร้าง skill

### 01 — Skill Anatomy (โครงสร้าง)

- [[SKILL.md structure]] — องค์ประกอบของไฟล์ SKILL.md
- [[YAML frontmatter]] — name, description, compatibility
- [[Description writing]] — เขียน description ให้ trigger ตรงจุด
- [[Bundled resources]] — scripts/, references/, assets/

### 02 — Workflow (ขั้นตอนการสร้าง)

- [[1. Capture intent]]
- [[2. Interview and Research]]
- [[3. Write SKILL.md]]
- [[4. Test cases and Evaluation]]
- [[5. Iteration loop]]
- [[6. Description optimization]]

### 03 — Best Practices

- [[Progressive disclosure]] — ลำดับการโหลดข้อมูล 3 ระดับ
- [[Writing style]] — สไตล์การเขียนที่ทำให้ skill ทำงานดี
- [[Examples and Patterns]] — pattern ที่ใช้ซ้ำได้
- [[Common mistakes]] — ข้อผิดพลาดที่ควรหลีกเลี่ยง

### 04 — Templates (สำหรับสร้าง note ใหม่)

- [[Templates/Skill Note Template]]
- [[Templates/Test Case Template]]

### 05 — References

- [[Skill creator notes]] — สรุปจาก skill-creator
- [[Useful tools and links]]

---

## 🐳 Docker Skills

| ชื่อ | โฟลเดอร์ | หน้าที่ |
|---|---|---|
| [[Docker/n8n-mysql/SKILL\|n8n-mysql]] | `Docker/n8n-mysql` | แก้ปัญหา n8n MySQL node ใน Docker — ETIMEDOUT, subnet conflict |

---

## 🤖 Machine-learning Skills

| ชื่อ                       | โฟลเดอร์                   | หน้าที่                                         |
| -------------------------- | -------------------------- | ----------------------------------------------- |
| [[Alpha/SKILL\|Alpha]]     | `Machine-learning/Alpha`   | Agent architecture — Claude API tool use loop   |
| [[Bravo/SKILL\|Bravo]]     | `Machine-learning/Bravo`   | ML domain knowledge — EDA, training, evaluation |
| [[Charlie/SKILL\|Charlie]] | `Machine-learning/Charlie` | Report generation — เลือก plot ตามโมเดล         |
|                            |                            |                                                 |

### Reports

- [[Charlie/ML Report - Defect Prediction\|ML Report - Defect Prediction]] — DOE/RSM dataset (2026-05-13)

---

## 🔬 SPC Skills

| ชื่อ | โฟลเดอร์ | หน้าที่ |
|---|---|---|
| [[SPC/spc-pdf-note/SKILL\|spc-pdf-note]] | `SPC/spc-pdf-note` | อ่าน PDF สแกน (render ผ่าน WinRT) → สรุปเป็น `.md` mirror D:\SPC↔Obsidian → อัปเดต hub note/daily log → สกัด diagram → ทำ interactive mind map (bundled `scripts/render-pdf.ps1`, `assets/mindmap-template.html`) |

---

## 🧩 Tooling Notes

| ชื่อ | โฟลเดอร์ | หน้าที่ |
|---|---|---|
| [[Claudian/install-guide\|Claudian install guide]] | `Claudian` | ติดตั้ง Claudian (Claude Code ใน Obsidian sidebar) บน Windows — gotcha: ไม่มีใน community store, id จริงคือ `realclaudian`, ตั้ง CLI path เอง, default เป็น YOLO mode |

---

## 🚀 Deployed to Claude Code

ติดตั้งแล้วที่ `~/.claude/skills/` บนเครื่อง Lamphun (2026-07-08) — ใช้งานได้จริงผ่าน `/skill-name` ทุก session:

| Skill folder ใน vault | ติดตั้งเป็นชื่อ | สถานะ |
|---|---|---|
| `DI-Agent-RAG/skill.md` | `di-agent-rag` | ✅ ติดตั้งแล้ว |
| `Docker/n8n-mysql/SKILL.md` | `n8n-docker-mysql` | ✅ ติดตั้งแล้ว |
| `Machine-learning/Alpha/SKILL.md` | `ai-agent-ml` | ✅ ติดตั้งแล้ว |
| `Machine-learning/Bravo/SKILL.md` + `assets/` | `machine-learning` | ✅ ติดตั้งแล้ว |
| `Machine-learning/Charlie/SKILL.md` | `ml-report` | ✅ ติดตั้งแล้ว |
| `SPC/spc-pdf-note/SKILL.md` + `scripts/` + `assets/` | `spc-pdf-note` | ✅ ติดตั้งแล้ว |
| `OEE/skill.md` | — | ❌ ยังไม่ใช่ skill จริง (ไม่มี YAML frontmatter — เป็นแค่ project note) |

---

## 🏷️ Tags หลัก

- `#MOC` — index
- `#skill/workflow` — ขั้นตอน
- `#skill/anatomy` — โครงสร้าง
- `#skill/best-practice`
- `#skill/template`
- `#skill/reference`

---

## 🎯 Quick Start

ถ้าเพิ่งเริ่มต้น แนะนำให้อ่านตามลำดับ:

1. [[What is a Skill]]
2. [[SKILL.md structure]]
3. [[1. Capture intent]]
4. [[3. Write SKILL.md]]
5. [[Progressive disclosure]]

---

## 📝 บันทึกการเปลี่ยนแปลง

- 2026-05-13: สร้าง vault ครั้งแรก
- 2026-05-13: เพิ่ม Machine-learning skills (Alpha, Bravo, Charlie) และ restructure folder
- 2026-07-08: ติดตั้ง 5 skills (di-agent-rag, n8n-docker-mysql, ai-agent-ml, machine-learning, ml-report) เข้า `~/.claude/skills/` บนเครื่อง Lamphun — ใช้งานได้แล้วผ่าน Claude Code ทุก session; mirror vault มาไว้ที่ `D:\Obsidian\Thadaverse\Projects\Skill-md` (ก่อนหน้านี้มีแค่บน GitHub)
- 2026-07-08 (เย็น): สร้าง skill ใหม่ `SPC/spc-pdf-note` จากงานสรุป AIAG SPC Chapter 1 วันนี้ (PDF สแกน → WinRT render → สรุป `.md` mirror → mind map) ติดตั้งเข้า `~/.claude/skills/` แล้ว และเพิ่มเข้า vault + ตาราง deployment
- 2026-07-16: เพิ่ม `Claudian/install-guide` — คู่มือติดตั้ง Claudian (Claude Code ใน Obsidian) แบบพกพา สำหรับใช้ตอนติดตั้งบนเครื่องอื่น
