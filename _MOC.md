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
| [[SPC/spc-abnormality-note/SKILL\|spc-abnormality-note]] | `SPC/spc-abnormality-note` | สืบสวนปัญหา/abnormality จากไฟล์ Excel: ดึงข้อมูลมาวิเคราะห์ผ่าน Excel COM (ตรวจสอบงานเดิมก่อนต่อยอด) → สกัดรูปกราฟจาก Shape objects → สรุปเป็น `.md` mirror พร้อม root-cause + Mermaid work-flow diagram (แยกเป็นแผนภาพเล็กถ้ากว้างเกิน) → อัปเดต hub note/daily log |
| [[SPC/spc-weekly-report/SKILL\|spc-weekly-report]] | `SPC/spc-weekly-report` | รวบรวม daily log ของสัปดาห์ → สร้าง weekly summary `.md` → สร้างไฟล์ Excel รายงานรูปแบบเดียวกับสัปดาห์ก่อนใน `X:\QM\IMS\Thada\Report\WeekN\` → sync 3 ทาง (vault ↔ D:\SPC\notes\ ↔ external report) |

---

## 🛠️ Engineering Skills

| ชื่อ | โฟลเดอร์ | หน้าที่ |
|---|---|---|
| [[Engineering/debug-mantra/SKILL\|debug-mantra]] | `Engineering/debug-mantra` | วินัย debug 4 ขั้นตอน: reproduce → trace the fail path → falsify the hypothesis → cross-reference every breadcrumb |
| [[Engineering/post-mortem/SKILL\|post-mortem]] | `Engineering/post-mortem` | เขียนบันทึก root cause/mechanism/fix/validation/how it slipped through หลัง debug เสร็จ |
| [[Engineering/qwen-agent/SKILL\|qwen-agent]] | `Engineering/qwen-agent` | ส่งงาน coding ที่ทำซ้ำ/ไม่ซับซ้อนไปให้ subagent Qwen (`claude-9arm`) ทำแทน ประหยัด token |
| [[Engineering/scrutinize/SKILL\|scrutinize]] | `Engineering/scrutinize` | รีวิว plan/PR/code แบบมองจากมุมคนนอก ตั้งคำถาม intent ก่อน แล้ว trace code path จริง |

ที่มา: [thananon/9arm-skills](https://github.com/thananon/9arm-skills) — `skills/engineering`

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
| `SPC/spc-abnormality-note/SKILL.md` | `spc-abnormality-note` | ✅ ติดตั้งแล้ว |
| `SPC/spc-weekly-report/SKILL.md` | `spc-weekly-report` | ✅ ติดตั้งแล้ว |
| `OEE/skill.md` | — | ❌ ยังไม่ใช่ skill จริง (ไม่มี YAML frontmatter — เป็นแค่ project note) |
| `Engineering/debug-mantra/SKILL.md` | `debug-mantra` | ✅ ติดตั้งแล้ว |
| `Engineering/post-mortem/SKILL.md` | `post-mortem` | ✅ ติดตั้งแล้ว |
| `Engineering/qwen-agent/SKILL.md` | `qwen-agent` | ✅ ติดตั้งแล้ว |
| `Engineering/scrutinize/SKILL.md` | `scrutinize` | ✅ ติดตั้งแล้ว |

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
- 2026-07-15: clone 4 skills จาก [thananon/9arm-skills](https://github.com/thananon/9arm-skills) `skills/engineering` (debug-mantra, post-mortem, qwen-agent, scrutinize) เข้า `~/.claude/skills/` บนเครื่อง Lamphun และเพิ่มเข้า vault ที่ `Engineering/` + ตาราง deployment
- 2026-07-15 (เย็น): สร้าง skill ใหม่ `SPC/spc-abnormality-note` จากงานวิเคราะห์ XPort LED miss-judgment วันนี้ (Excel COM data pull → verify/extend ANOVA-GRR → root-cause note พร้อม Mermaid flow diagram) ติดตั้งเข้า `~/.claude/skills/` แล้ว และเพิ่มเข้า vault + ตาราง deployment — เก็บ Excel COM gotchas (orphan process/lock file, Int32 cast bug, leading "=" text bug, PowerShell case-insensitive variable collision) และบทเรียนเรื่อง Mermaid flow diagram ไว้ในตัว skill ด้วย
- 2026-07-17: สร้าง skill ใหม่ `SPC/spc-weekly-report` จากงานทำรายงานประจำสัปดาห์ส่งหัวหน้า (Week2) — รวบรวม daily log → weekly summary note → Excel รายงานรูปแบบเดียวกับสัปดาห์ก่อนใน `X:\QM\IMS\Thada\Report\WeekN\` → sync 3 ทาง (vault/D:\SPC\notes\/external report) ติดตั้งเข้า `~/.claude/skills/` แล้ว และเพิ่มเข้า vault + ตาราง deployment — บันทึกบทเรียนเรื่องลืม mirror `D:\SPC\notes\weekly\` ไว้ในตัว skill ด้วยกันพลาดซ้ำ
- 2026-08-04: อัปเดต `Machine-learning/Bravo` (`machine-learning` skill) จากงาน PyCaret anomaly-detection benchmark สำหรับปัญหา miss-judgment XPort LED ([[pycaret-anomaly-comparison-2026-08-04]] ใน `Projects/SPC/abnormal/miss judgement/`) — เพิ่ม section "PyCaret (AutoML multi-algorithm benchmark)": วิธีสร้าง conda env แยกให้ถูกต้อง (`--override-channels -c conda-forge` กัน Anaconda ToS block, วิธีแก้ ZstdError จาก RAM ต่ำ), gotcha เรื่อง `sod` algorithm crash ใน `pyod`, และข้อจำกัดของ `pycaret.anomaly.plot_model()`/`dashboard()`/`create_app()` (ใช้ได้เฉพาะ classification/regression module) เพิ่ม asset ใหม่ `assets/pycaret_anomaly_template.py` และปรับ description ให้มีคำว่า "pycaret"/"AutoML"/"anomaly detection" — sync กับ `~/.claude/skills/machine-learning/` แล้ว ยังไม่ commit ขึ้น GitHub
