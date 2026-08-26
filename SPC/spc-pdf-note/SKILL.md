---
name: spc-pdf-note
description: ใช้ skill นี้เมื่อ Thada ให้ไฟล์ PDF (โดยเฉพาะสแกน ไม่มี text layer เช่น AIAG manual, Hana Flow, work instruction) แล้วขอให้อ่าน/สรุปเป็นความรู้เก็บไว้ใน SPC knowledge base — ครอบคลุมขั้นตอน render PDF เป็นภาพด้วย Windows.Data.Pdf WinRT API (ไม่ต้องติดตั้ง poppler), หาขอบเขตบท/หน้าจากสารบัญ, อ่านทีละหน้าด้วย multimodal Read, เขียนสรุปเป็น .md แบบผสมไทย+อังกฤษ เก็บใน Obsidian vault เป็น source of truth เดียว (ไม่ mirror เข้า D:\SPC อีกต่อไป), อัปเดต hub note + daily log, สกัด diagram สำคัญมาแนบ, และสร้าง interactive mind map สไตล์ PCB-trace ถ้าต้องการ — trigger เมื่อพูดถึง "สรุป PDF", "อ่านหนังสือ SPC", "สรุปบทที่...", "ทำ mind map", หรือให้ไฟล์ PDF ในโฟลเดอร์ D:\SPC\research
---

# SPC PDF → Knowledge Note (+ optional mind map)

ขั้นตอนมาตรฐานสำหรับอ่านเอกสาร PDF (ส่วนใหญ่เป็นสแกน ไม่มี text layer) แล้วสรุปเข้า knowledge base ของ Thada ใน Obsidian vault `D:\Obsidian\Thadaverse\Projects\SPC` — vault คือ source of truth เดียวสำหรับ note `.md` ทั้งหมด (ไม่ mirror เข้า `D:\SPC` อีกต่อไป) ส่วน `D:\SPC` เก็บเฉพาะไฟล์ทำงานดิบ (PDF ต้นฉบับใน `research\`, Excel summary ใน `summaries\`)

## 0. เช็ค convention ที่มีอยู่ก่อนเสมอ

อ่าน `D:\Obsidian\Thadaverse\Projects\SPC\SPC Home.md` และไฟล์ `daily\` ล่าสุดก่อน เพื่อดูว่าหัวข้อนี้เคยสรุปไปหรือยัง และ convention ปัจจุบันเป็นแบบไหน (บางเอกสารอาจตกลง convention เฉพาะกับ Thada ไว้แล้ว เช่น "แยกไฟล์ต่อบท", "ไม่มี Excel summary" — อย่าถือว่า convention ของเอกสารหนึ่งใช้กับทุกเอกสาร)

## 1. ตรวจว่า PDF อ่าน text ตรงได้ไหม

ลอง `Read` tool กับไฟล์ PDF ปกติก่อน (ใส่ `pages` ถ้าไฟล์ยาวเกิน 10 หน้า) ถ้าเจอ error แบบ `pdftoppm is not installed` แปลว่าเป็น PDF สแกน/ไม่มี text layer — ไปขั้นตอนที่ 2

## 2. Render หน้า PDF เป็นภาพด้วย WinRT

เครื่องนี้ไม่มี poppler-utils ให้ใช้ `scripts/render-pdf.ps1` (bundled ใน skill นี้) แทน — ใช้ Windows.Data.Pdf WinRT API ผ่าน PowerShell reflection helper (ไม่ต้องติดตั้งอะไรเพิ่ม)

```powershell
powershell.exe -File "<skill-dir>/scripts/render-pdf.ps1" `
  -PdfPath "D:\SPC\research\ชื่อไฟล์.pdf" `
  -OutDir "<scratchpad>\pdf-pages" `
  -StartPage 1 -EndPage 15
```

ต้องรันผ่าน `powershell.exe -File` (ไม่ใช่ `-Command` แบบ inline) เพราะ script มีตัวแปรและ reflection ที่ซับซ้อน สคริปต์ปริ๊นท์ `PageCount` รวมของ PDF ให้ทราบด้วยตอนรันครั้งแรก

## 3. หาขอบเขตหน้าที่ต้องการ

- Render หน้าแรกๆ (~15-20 หน้า) ก่อนเพื่อหาสารบัญ (Table of Contents) แล้วอ่านด้วย multimodal `Read` ทีละภาพ
- **สำคัญ**: เลขหน้าไฟล์ PDF (physical page) มักไม่ตรงกับเลขหน้าพิมพ์ในเล่ม (front matter เช่น i, ii, iii... มาก่อน) ต้องคำนวณ offset เอง โดยดูจากเลขหน้าที่พิมพ์อยู่จริงในแต่ละภาพเทียบกับลำดับไฟล์
- **เช็ค offset ซ้ำเป็นระยะ** อย่าคำนวณครั้งเดียวแล้วเชื่อตลอดทั้งเล่ม — PDF สแกนบางไฟล์ขาดหน้าไปโดยไม่รู้ตัว (เจอมาแล้วกับ AIAG SPC manual: ขาด 2 หน้าตรงกลาง Chapter 1 เพราะสแกนพลาด) วิธีตรวจ: ถ้า physical page ต่อเนื่องกันแต่เลขหน้าพิมพ์กระโดดข้าม ให้สงสัยว่าขาดหน้า เทียบ `PageCount` ทั้งไฟล์กับจำนวนหน้าที่เอกสารควรมีจริง (เช่นจาก List of Illustrations/Index ท้ายเล่ม) ถ้าไม่ตรงกันแปลว่าขาด — บันทึกเป็นหมายเหตุในสรุปด้วย อย่าละเลย

## 4. Render และอ่านช่วงที่ต้องการ

Render เป็นชุด (ครั้งละ ~10-20 หน้าต่อ PowerShell call ก็ได้ ไม่จำกัดเหมือน Read tool) แล้วอ่านด้วย multimodal `Read` ทีละภาพ เรียงตามลำดับ — เรียก Read หลายไฟล์พร้อมกันได้ในเดียวกัน (parallel tool calls) เพื่อความเร็ว แต่ผลลัพธ์จะกลับมาตามลำดับที่เรียก ใช้ตรวจสอบ offset ได้ด้วย

## 5. เขียนสรุปเป็น `.md`

**ที่ตั้งไฟล์ (source of truth เดียว):**
```
D:\Obsidian\Thadaverse\Projects\SPC\knowledge\<slug>.md
```

**กฎเนื้อหา (ยืนยันกับ Thada แล้ว ใช้เป็นค่าเริ่มต้น):**
- เขียนแบบ**ผสมไทย + ศัพท์เทคนิคอังกฤษ** (ไม่ใช่ไทยล้วน ไม่ใช่อังกฤษล้วน)
- ต้องมี backlink `🏠 [[SPC Home]]` อยู่ต้นไฟล์เสมอ
- ถ้าเอกสารเป็น**หนังสือ/manual หลายบท**: ถามหรือ default เป็น **แยกไฟล์ต่อบท** (`<slug>-ch1-...`, `<slug>-ch2-...`) เพื่อกันไฟล์ยาวเกินไป
- ถ้าเอกสารเป็น**สไลด์บริษัท/เอกสารหัวข้อเดียว** (เช่น orientation deck): ไฟล์เดียวแบ่งหัวข้อด้วย heading ก็พอ
- **ถามผู้ใช้ก่อนเริ่มเขียน** (อย่าเดาเอง) 3 เรื่องนี้ถ้ายังไม่เคยตกลงไว้กับเอกสารนี้มาก่อน:
  1. โครงสร้างไฟล์ (รวมเล่มเดียว vs แยกต่อบท)
  2. จะแนบภาพ/diagram จากต้นฉบับไหม (และถ้าแนบ กี่ภาพต่อ section — แนวทางเดิมคือ ~1 ภาพต่อหัวข้อใหญ่ ไม่ต้องครบทุกหน้า)
  3. ต้องการไฟล์ Excel summary คู่กันไหม (`D:\SPC\summaries\*.xlsx`, project-only ไม่ mirror ไป Obsidian)
- ปิดท้ายไฟล์ด้วยบรรทัด **Conversation reference** สั้นๆ บอกวันที่สรุปและขอบเขตหน้าที่ครอบคลุม + สิ่งที่ยังไม่ได้ทำ (บทถัดไป ฯลฯ)

## 6. อัปเดต hub note และ daily log

- เพิ่มลิงก์ `[[<slug>]]` แบบ wikilink จริง (ไม่ใช่ plain text) ในส่วน `## Knowledge` ของ `SPC Home.md` — plain-text ไม่สร้าง graph edge ใน Obsidian
- อัปเดต/สร้าง `daily\YYYY-MM-DD.md` บันทึกว่าทำอะไร, key finding, งานค้าง, next step — ตาม pattern ของไฟล์ daily log เดิม

## 7. (ถ้าต้องการ) สกัดภาพ diagram สำคัญ

ถ้า Thada ต้องการภาพประกอบ:
- เลือกเฉพาะ diagram/figure สำคัญ (~1 ภาพต่อ section ใหญ่ ไม่ต้องทุกหน้า) จากภาพที่ render ไว้แล้วในขั้นตอนที่ 4 — ไม่ต้อง crop ก็ได้ ใช้ full-page render ตรงๆ ได้เลย (เป็น pattern ที่ใช้มาตลอด)
- Copy ไปที่ `Projects\SPC\knowledge\assets\NN-descriptive-name.png` ใน vault (ตั้งชื่อบรรยาย ไม่ใช้ `page-0XX.png`)
- อ้างอิงในเนื้อหา `.md` ด้วย markdown ธรรมดา `![alt](assets/NN-descriptive-name.png)` (**ห้าม** ใช้ Obsidian wikilink embed `![[ ]]`) เพื่อให้ภาพขึ้นทั้งใน Obsidian และตอนเปิดไฟล์ธรรมดา — วางรูปไว้เหนือย่อหน้าที่เกี่ยวข้องกับ diagram นั้น

## 8. (ถ้าต้องการ) สร้าง interactive mind map

ถ้า Thada ขอ mind map แบบ interactive (เคยทำมาแล้วสำหรับ company-overview และ AIAG SPC Chapter 1):

1. Copy `assets/mindmap-template.html` (bundled ใน skill นี้) ไปเป็นไฟล์ปลายทางที่ `Projects\SPC\knowledge\assets\<slug>-mindmap.html`
2. แก้ 4 จุดที่ comment กำกับไว้ในไฟล์ (`EDIT 1`-`EDIT 4`): header text, hint text, legend labels, และ `const DATA` tree
3. ออกแบบ `DATA` tree จากเนื้อหาที่สรุปไว้แล้วใน `.md` — แนะนำ **4 กิ่งหลัก (L1)** เพื่อความสมดุลของภาพ, เก็บ label สั้น (2-4 คำต่อบรรทัด, node กว้างคงที่ 236px), ใส่ `detail` ทุก node ที่มีเนื้อหาจริง (คลิกแล้วเปิด panel), `tag` เป็น section reference (เช่น `"SECTION E"`)
4. ถ้ามีรูปจากขั้นตอนที่ 7 อยากให้โผล่ใน mind map ด้วย: แปลงเป็น base64 แล้วใส่เป็น `img: ["data:image/png;base64,..."]` ในโหนดที่เกี่ยวข้อง — **อย่า paste base64 ยาวๆ ผ่าน Edit/Write tool ตรงๆ** (กิน context มหาศาล) ให้เขียน PowerShell script อ่านไฟล์รูปด้วย `[System.IO.File]::ReadAllBytes` + `[Convert]::ToBase64String` แล้วต่อ string เข้าไฟล์ HTML ด้วย `[System.IO.File]::ReadAllText`/`WriteAllText` (UTF8 no-BOM) แทน — ดูตัวอย่าง pattern ได้จาก daily log 2026-07-08 ถ้าต้องการ
5. เปิดด้วย `Start-Process "<path>"` เพื่อตรวจดูก่อนแจ้งผู้ใช้ว่าเสร็จ

## หมายเหตุสภาพแวดล้อม (เครื่องนี้)

- ไม่มี poppler-utils/pdftoppm, ไม่มี python/openpyxl, ไม่มี ImportExcel — ห้ามพึ่งพาสิ่งเหล่านี้
- Excel summary (ถ้าต้องทำ) ใช้ Excel COM automation (`New-Object -ComObject Excel.Application`) ได้ผลดี
- **PowerShell script encoding gotcha**: `powershell.exe -File script.ps1` มักอ่านตัวอักษรไทยใน string literal ที่เขียนผ่าน Write tool ผิด (mojibake) เพราะ encoding mismatch — เขียนเนื้อหาภาษาไทยผ่าน Write/Edit tool ลงไฟล์ `.md`/`.html` โดยตรงเสมอ อย่า inline ภาษาไทยใน `.ps1` string ที่จะรันผ่าน `-File`
- ไฟล์ `.md`/`.html` ที่ต้องรองรับภาษาไทยให้เขียนผ่าน Write/Edit tool (ซึ่ง encode UTF-8 ถูกต้อง) ไม่ใช่ผ่าน PowerShell string
