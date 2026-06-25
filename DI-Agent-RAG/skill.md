---
name: di-agent-rag
description: "แนวทาง debug/ปรับปรุง n8n RAG workflow ของ DI-Agent (Dicing factory) — Qdrant + Ollama + Docling. ใช้เมื่อ AI ตอบผิดเอกสาร/ตอบไม่ครบ/รูปผิด/route ผิด/text-to-SQL เพี้ยน"
metadata:
  type: project-skill
  stack: n8n, Qdrant, Ollama, Docling, MySQL
---

# DI-Agent RAG (n8n) — Skill Note

## Context

n8n workflow RAG สำหรับโรงงาน Dicing — ตอบคำถามจากเอกสาร SOP (DOC), query ฐานข้อมูล (SQL), WIP/MC/PT/OEE
ไฟล์หลัก: `D:\AI-project\docker\project\OEE Cache v2 RAG.json`

> n8n โหลด workflow เข้า database ของตัวเอง → **แก้ไฟล์แล้วต้อง re-import** (Import from File ทับ workflow เดิม → Save → ปิด-เปิด Active) ส่วน **Qdrant แก้แล้วมีผลทันที**

---

## Tech Stack

| Layer | Tech |
|-------|------|
| Orchestration | n8n (Code node = task-runner sandbox: ห้าม fetch/require/`$helpers`) |
| Vector DB | Qdrant `:6333` collection `multi-modal` |
| Embedding | Ollama `bge-m3:latest` |
| Generation | Ollama `qwen2.5:7b` (num_ctx 32768, temp 0.1) |
| Doc extract | Docling (`:5001`) |
| Images | nginx static `:8089` → `shared/extracted-images` |
| SQL | MySQL (oe_dicing, qtsoft, vipdatabase) |

## DOC Pipeline

`DOC Embed → DOC Search Qdrant (limit 100) → DOC Scroll Qdrant (500) → DOC Format Prompt → DOC LLM Call → DOC Append Images → Respond`

---

## บทเรียนหลัก / Key Patterns (นำไปใช้ซ้ำได้)

### 1. รูปภาพ (Append Images)
- **ผูกรูปกับ answer source = เอกสารของ chunk อันดับ 1 (rank-1)** ดึงรูปเฉพาะจาก source นั้น (score ≥ 0.45)
- ❌ อย่าใช้ "summed-dominant score" → เอกสารใหญ่ (เช่น Rev.21 309 chunks) จะชนะทุกคำถาม
- ❌ PDF section ของ Docling = header/footer ขยะ ("AGC Group Internal Use", "Page x of y") → **อย่า section-scope**
- chunk รูปต้องมี "ข้อความบรรยาย" ถึงจะ rank ได้ (PDF ดีกว่า xlsx เพราะ Docling ผูกรูปกับ text)

### 2. Chunking / Ingestion
- **ไฟล์ MD ที่ทำมือ (ตาราง) ห้ามผ่าน Docling** → มันแตกตารางเป็น row junk + ซ้ำ ~9 เท่า → insert ตรงเข้า Qdrant เอง chunk ตาม `## section`
- **Dedup Qdrant** เป็นระยะ: ลบ content ซ้ำใน source เดียวกัน (เคยลด 1664 → 563)
- หน้า flowchart/scan ที่ Docling OCR ไม่ออก → **ถอดข้อความเอง (Claude อ่านรูปได้) ใส่ chunk + ฝัง image URL inline**

### 3. Context completeness (Format Prompt)
- เอา chunk จาก answerSrc มาก่อน, **dedup ก่อน slice** (ไม่งั้น section หาย), char budget ~22000
- trigger expand: `ทุก|ทั้งหมด` / method (`วิธี|ขั้นตอน`) / spec → ดึงจาก scroll เติมให้ครบ
- spec "ทั้งหมด" → table-first จะได้ครบทุก category

### 4. Routing (Parse Route)
- **regex keyword override เอาชนะ AI router** (AI เดาพลาดบ่อย)
- data query (`defect|yield|ย้อนหลัง|css`) → SQL ; method/troubleshoot → DOC
- **normalize `AD 31` → `AD31`** (เว้นวรรค) ทั้งใน routing และ query literal

### 5. Text-to-SQL มี 3 ชั้น (ระวังตีกันเอง)
1. **SQL Agent** (prompt/LLM) เขียน query
2. **SQL-request** (Code) มี intercept ที่ **เขียน query ทับ** — "AI เขียนถูกแต่ output เปลี่ยน" = ชั้นนี้
3. **cleanSQL** rebuild WHERE — ต้องรองรับ `MCNo IN (...)` ไม่งั้นตัดทิ้ง
- กฎ: ระบุเครื่อง ADxx → `master mc ad_ program` ; ถาม product รันเครื่องไหน → `adyield`

### 6. Generation (qwen2.5:7b)
- หลุดภาษาจีนเมื่อเจอ context OCR กระจัดกระจาย → กฎ Thai-only แบบ **bilingual (อังกฤษ+ไทย)** + **strip CJK** ใน Append Images (`[一-鿿぀-ヿ㐀-䶿　-〿＀-￯]`)
- TYPE A (lookup) vs TYPE B (stats) → **classify ใน code (Prep Analysis Data) จาก columns** ไม่ปล่อยให้ LLM เดา (MCNo/IP/Version → A ตอบสั้น, DateA/defect → B วิเคราะห์เต็ม)

### 7. Process flow vs Glass type
- chunk product สั้น (`## PDX`) outrank chunk process flow → ใส่ **intent boost**: query "process flow" → ดัน `processflow.md` ขึ้นก่อน

---

## วิธี Debug (mantra: reproduce → trace → falsify → breadcrumb)

- **Reproduce กับ Qdrant/Ollama จริงด้วย Node script ก่อนแก้เสมอ** (อย่าเดา)
- **Thai encoding**: เขียน Node script ลงไฟล์ผ่าน Write tool (UTF-8) แล้ว `node file` — **ห้าม pipe ไทยผ่าน PowerShell** (กลายเป็น `?????`)
- **แก้ JSON**: ใช้ Node `JSON.parse/stringify` — ห้าม PowerShell `ConvertTo-Json`
- **Qdrant ผ่าน Node http** ไป `localhost:6333` (PowerShell sandbox block path ที่มี `/collections/` หรือ `?wait=true`)
- แก้ jsCode เลี่ยง escape นรก: เขียน code จริงลงไฟล์ `.js` แยก แล้วให้ script เซ็ต `node.parameters.jsCode = readFileSync(...)`

---

## Pitfalls

- PowerShell pipe + ไทย → mojibake `?????` ; ใช้ `[System.IO.File]::WriteAllText(path, content, UTF8)`
- Re-ingest MD ทำมือผ่าน Docling = junk + dup กลับมา → เอาออกจาก `rag-files/pending`
- Qdrant source path เป็น full path (`/data/rag-files/pending/...`) ไม่ใช่ชื่อไฟล์
- ลบไฟล์ใน `processed/` ไม่ลบ chunk ใน Qdrant (คนละชั้น)
- num_ctx overflow ถ้า context > ~60K chars → จำกัด budget ~22K

---

## Image Hosting (deployment) — สำคัญ

รูปต้องเสิร์ฟจาก **origin เดียวกับ UI** ไม่งั้น user เห็นรูปไม่ได้
- UI อยู่ที่ `http://172.18.106.100:8888/DI-Agent/` (PHP) ; `formatMarkdown` แปลง `![](url)` → `<img src=url>` → browser user ต้องเข้าถึง url นั้น
- ❌ ห้ามชี้ url ไปเครื่อง dev/docker (`172.18.113.242:8089`) — คนละ subnet, user เข้าไม่ถึง
- ✅ รูปอยู่ `\\172.18.106.100\www\DI-Agent\images\` → url `http://172.18.106.100:8888/DI-Agent/images/...` (same-origin, ไม่มี CORS)
- URL base ตั้งใน Local file watcher node **"Transform Image Paths"** (เอกสารใหม่) + rewrite ใน Qdrant (เอกสารเก่า)
- **n8n container เขียน SMB share ไม่ได้** (เห็นแค่ volume) → ต้อง `robocopy extracted-images → share` ที่ **host** หลัง ingest
- สถาปัตยกรรม UI: file-queue relay (`proxy.php` เขียน .req ลง share → relay_client บน dev อ่านส่ง n8n → เขียน .res) เพราะ web server เข้า n8n ตรงไม่ได้

## VLM Captioning (แก้ textless image)

figure ที่ฝังข้อความในรูป (flowchart/ตาราง scan) → Docling ได้ chunk **ไร้ข้อความ** (`# [IMG][IMG]`) → search ไม่เจอ → ไม่เคยถูกแนบ
- ตรวจ: count chunk ที่มีรูป แต่ text < 25 ตัวอักษร (เคยเจอ 17 chunks / ~73 รูป)
- **กรองด้วยขนาดไฟล์**: ≥40KB = figure จริง (~22 รูป), <40KB = ลายน้ำ/ป้าย ("For Reference"/"CORRECT") ข้าม
- แก้ = caption ด้วย **local VLM `qwen2.5vl:7b`** (offline — เอกสาร internal ห้าม API ออก): โหลดรูป → caption ไทย → prepend เป็นข้อความ → re-embed → upsert ทับ id เดิม (post-process ไม่ต้อง re-ingest)
- VLM caveats: หลุดภาษาจีน (ต้อง strip CJK) ; บางทีผิด logic (เช่น สลับ % ใน flowchart)
- ปัจจุบันเป็น **script รันมือ** ไม่ได้อยู่ใน pipeline — เอกสารใหม่ต้องรันซ้ำ (หรือ integrate เป็น node ใน watcher / เปิด Docling `do_picture_description`)
- ทางเลือกถ้า VLM คุณภาพไม่พอ: ถอด flowchart มือ (Claude อ่านรูปได้) + ฝัง image inline แบบ polymer/uncut/scrap

---

## Conversation Reference

สร้าง: 2026-06-24 | อัปเดต: 2026-06-25

แก้หลักตลอด session:
- รูป: dominant-source → rank-1 answerSrc + PDF-aware
- เพิ่ม product_glass_type.md, processflow.md, spec_control.md (insert ตรง, dedup)
- routing: AD-space, data→SQL, scrap/uncut/version keywords
- text-to-SQL: RULE intercept guard + cleanSQL IN(...) + machine literal normalize
- generation: Thai-only แรงขึ้น + CJK strip ; TYPE A/B deterministic
- transcribe flowchart (uncut image_000005 / scrap NG image_000003) เป็น chunk + รูป
- rebuild processflow.md จาก table junk เป็น 13 clean chunks + intent boost
- (รอบ 2) Append Images: rank-1 answerSrc + กรอง revision-history chunk + overlap re-rank ตามคำตอบ
- (รอบ 2) ย้าย image hosting → www server (172.18.106.100:8888) + rewrite URL ใน Qdrant + Local file watcher
- (รอบ 2) VLM captioning textless figures (qwen2.5vl:7b, ≥40KB) — textless 17→9
- (รอบ 2) วินิจฉัย: รูป polymer ไม่เคยถูกเพราะ image_000035 อยู่ chunk ไร้ข้อความ ; qwen2.5:7b ไม่เสถียร (สุ่มหลุดจีน) แต่ user เลือกคงไว้
