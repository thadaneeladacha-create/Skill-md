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
