---
tags:
  - skill/reference
title: Skill creator notes
created: 2026-05-13
---

# Skill Creator — สรุป

> Meta-skill ที่ Anthropic ให้มาสำหรับสร้าง skill อื่น ๆ

## Capabilities หลัก

- สร้าง skill ใหม่
- แก้/ปรับปรุง skill ที่มีอยู่
- รัน evaluation + benchmark
- Optimize description

## Scripts สำคัญ

### `scripts.aggregate_benchmark`

รวมผล eval ของ iteration หนึ่งให้เป็น `benchmark.json` + `benchmark.md`

```bash
python -m scripts.aggregate_benchmark <workspace>/iteration-N \
  --skill-name <name>
```

### `eval-viewer/generate_review.py`

เปิด HTML viewer ให้ผู้ใช้ review outputs:

```bash
python <skill-creator>/eval-viewer/generate_review.py \
  <workspace>/iteration-N \
  --skill-name "my-skill" \
  --benchmark <workspace>/iteration-N/benchmark.json
```

ใน Cowork / headless: ใช้ `--static <output>`

### `scripts.run_loop`

Optimize description อัตโนมัติ:

```bash
python -m scripts.run_loop \
  --eval-set <eval.json> \
  --skill-path <skill> \
  --model <model-id> \
  --max-iterations 5
```

### `scripts.package_skill`

แพ็ก skill เป็น `.skill` file:

```bash
python -m scripts.package_skill <path/to/skill>
```

## Subagents

- `agents/grader.md` — ประเมิน assertion vs output
- `agents/comparator.md` — blind A/B comparison
- `agents/analyzer.md` — วิเคราะห์ว่าทำไม version หนึ่งดีกว่า

## References ของ skill-creator

- `references/schemas.md` — JSON schemas

## ไปต่อที่

- [[_MOC]]
- [[Useful tools and links]]
