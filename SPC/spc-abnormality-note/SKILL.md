---
name: spc-abnormality-note
description: ใช้ skill นี้เมื่อ Thada มีไฟล์ Excel ข้อมูล/ผลการทดลองของ abnormality หรือปัญหาที่ต้องสืบสวน (เช่น MoM, experiment data, measurement log) แล้วอยากให้ (1) ดึงข้อมูลจาก Excel มาวิเคราะห์/ตรวจสอบ/ต่อยอด (2) สรุปผลเป็น knowledge note ใน SPC knowledge base พร้อม work flow / root-cause diagram (3) สรุป root cause ให้ชัดเจน — trigger เมื่อพูดถึง "วิเคราะห์ไฟล์ abnormality", "ต่อยอด ANOVA/GRR ที่ทำไว้", "ทำ flow map สรุปปัญหา", "สรุป root cause ลง note", หรือให้ไฟล์ .xlsx ในโฟลเดอร์ D:\SPC\abnormal
---

# SPC Abnormality Investigation: Excel → Analysis → Root-Cause Note

ขั้นตอนมาตรฐานสำหรับสืบสวนปัญหา/abnormality ที่มีข้อมูลอยู่ใน Excel: ดึงข้อมูลมาวิเคราะห์ (ตรวจสอบงานเดิมของ Thada ก่อนเสมอถ้ามี), สรุปเป็น knowledge note พร้อม root-cause flow diagram, mirror เข้า `D:\SPC` + Obsidian ตาม convention เดิม

## 0. เช็ค convention ที่มีอยู่ก่อนเสมอ
อ่าน `D:\SPC\notes\SPC Home.md` และ `notes\daily\` ล่าสุดก่อน ดูว่าเรื่องนี้เคยมี note อยู่แล้วหรือยัง (ถ้ามี ให้ **อัปเดต note เดิม** ไม่สร้างไฟล์ใหม่ซ้ำ) และดูว่ามี action item ค้างเกี่ยวกับไฟล์นี้ไหม (เช่น ANOVA ที่ Thada ต้องทำส่ง)

## 1. ดึงข้อมูลจาก Excel มาวิเคราะห์

เครื่องนี้**ไม่มี python/openpyxl/pandas** — ใช้ Excel COM automation เสมอ (`New-Object -ComObject Excel.Application`)

**ก่อนเปิดไฟล์ทุกครั้ง (สำคัญมาก ดู §5 เรื่อง incident ที่เคยเกิด):**
```powershell
Get-Process EXCEL -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Milliseconds 300
Remove-Item "<folder>\~`$<filename>.xlsx" -Force -ErrorAction SilentlyContinue
```

**Dump sheet เป็น TSV เพื่ออ่าน/วิเคราะห์ด้วย PowerShell:**
```powershell
$wb = $excel.Workbooks.Open($path, 0, $true)   # 0=updatelinks, $true=ReadOnly ถ้าแค่จะอ่าน
$ws = $wb.Worksheets.Item("SheetName")
$vals = $ws.UsedRange.Value2
# loop rows/cols แล้ว join ด้วย tab, Set-Content -Encoding UTF8
```
ถ้าต้องคำนวณสถิติเพิ่ม (ANOVA, Gage R&R ฯลฯ) ให้ parse ค่าเป็น object แล้วคำนวณเองด้วย PowerShell (ดู pitfalls ใน §5 ก่อนเขียน loop)

**ตรวจสอบงานเดิมของ Thada ก่อนเสมอถ้ามี sheet วิเคราะห์อยู่แล้ว** — วิเคราะห์อิสระด้วยตัวเองก่อน แล้ว reproduce ตัวเลขของ Thada ให้ตรงเป๊ะก่อนจะบอกว่า "ถูก/ผิด" หรือต่อยอดเพิ่ม อย่าเชื่อ column header เดาโครงสร้าง experiment เอง — **ถ้าโครงสร้างข้อมูลไม่ชัด (เช่น กี่ physical unit จริง, unit ไหน crossed/nested กับปัจจัยไหน) ให้ถามผู้ใช้ตรงๆ ด้วย AskUserQuestion แทนการเดา** (session ก่อนเดาผิด 2 รอบเรื่องจำนวน physical unit — 40→2→8 — ก่อนจะถูกจริง เสียเวลาคำนวณซ้ำ)

ถ้าต้องเพิ่ม sheet ผลวิเคราะห์ลงไฟล์ Excel เดิม ใช้สูตร (`.Formula`) อ้างอิงกลับ raw data เสมอ ไม่ hardcode ตัวเลข (traceable) — ดู pattern ทำ Gage R&R nested ที่ [[nested-grr-excel]] skill (ระวัง: nested formula ใช้ไม่ได้กับ crossed design เช็คให้ถูกก่อน)

## 2. สกัดรูปประกอบจาก Excel (ถ้ามี chart/boxplot ต้นฉบับ เช่น จาก Minitab)

Chart ที่ paste มาจาก Minitab มักเป็น **Shape (Type=13, msoPicture)** ไม่ใช่ ChartObject ของ Excel — ใช้ `$ws.Shapes` ไม่ใช่ `$ws.ChartObjects()`:
```powershell
foreach ($sh in $ws.Shapes) { "{0} Left={1} Top={2} W={3} H={4}" -f $sh.Name,$sh.Left,$sh.Top,$sh.Width,$sh.Height }
```
ใช้ `Left`/`Top` ของ shape เทียบกับ `Cells.Item(1,col).Left` เพื่อหาว่า column ไหนคือขอบเขตจริงของกราฟ (กันไม่ให้ crop ติดตาราง/text คอลัมน์ข้างๆ มาด้วยโดยไม่ตั้งใจ — เกิดมาแล้วครั้งหนึ่ง ต้อง re-crop)

**Export range เป็นรูปภาพ:**
```powershell
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$rng.CopyPicture(1, 2)   # xlScreen, xlBitmap
Start-Sleep -Milliseconds 500
$img = [System.Windows.Forms.Clipboard]::GetImage()
$img.Save($outPath, [System.Drawing.Imaging.ImageFormat]::Png)
```
ถ้าต้องการรูปแยกทีละหัวข้อ (เช่นทีละ LED channel/parameter) หา row boundary แต่ละ block ด้วย `$ws.Cells.Find("keyword")` + `FindNext` วนหา address ทั้งหมดก่อน แล้วค่อย crop เป็นช่วงๆ

## 3. เขียนสรุปเป็น knowledge note (`.md`)

ตาม convention เดียวกับ [[spc-pdf-note]]:
```
D:\SPC\notes\knowledge\<slug>.md                          <- ต้นทาง
D:\Obsidian\Thadaverse\Projects\SPC\knowledge\<slug>.md    <- mirror, byte-identical
```
- ผสมไทย+อังกฤษ, มี `🏠 [[SPC Home]]` backlink ต้นไฟล์
- รูปที่สกัดมาเก็บที่ `notes\knowledge\assets\` (mirror เหมือนกัน) อ้างอิงด้วย `![alt](assets/xxx.png)` ธรรมดา ไม่ใช้ `![[ ]]`
- **สรุปให้กระชับ** — ใส่เฉพาะค่าสถิติสำคัญ (เช่น F/P/R-Sq/mean ranking) ไม่ต้องยกตาราง DF/SS/MS/Error เต็มทุกตัวเลข เว้นแต่ผู้ใช้ขอ ถ้าต้องการ CI ให้โชว์แบบ **visual** (เช่น ASCII CI-plot จาก Minitab ตรงๆ ในโค้ดบล็อก) ไม่ใช่ตัวเลข bracket ธรรมดา
- ถ้ามีรูปกราฟประกอบ (จาก §2) ให้รูปนั้นมีแค่ตัวกราฟ ไม่ต้องมีตาราง/text ค่าซ้ำกับที่สรุปเป็น text ไว้แล้วในเนื้อหา (กันข้อมูลซ้ำซ้อน)
- อัปเดต Action Items table ในไฟล์เดิม (ถ้ามี) แทนเขียนใหม่ — ระบุสถานะ "Completed (draft, รอ [ชื่อผู้รับผิดชอบ] review)" ถ้างานนี้ทำแทนคนอื่นเป็น draft ไม่ใช่ปิดงานเด็ดขาด

## 4. ทำ Work Flow / Root-Cause Map

**บทเรียนสำคัญเรื่อง flow diagram (เจอมาแล้วหลายรอบ):**
- ใช้ **Mermaid `flowchart TD`** (top-down) เป็นค่าเริ่มต้น — Thada ชอบแบบนี้มากกว่า ASCII tree (ลองมาแล้ว feedback คือ "ดูไม่เหมือน flow")
- **ห้ามย่อ/ตัดคำในตัว node เพื่อแก้ปัญหากราฟกว้างเกินจอ** (ลองแล้ว feedback คือ "แย่กว่าเดิม") — ให้คงข้อความเต็มทุกคำเสมอ
- ถ้ากราฟกว้างเกิน (หลายกิ่งขนานกันในระดับเดียว ทำให้ node ความกว้างรวมกันล้นจอ) ให้ **แยกเป็นแผนภาพเล็กหลายอันแทน** — 1 แผนภาพ mermaid ต่อ 1 กิ่งหลัก/ประเด็น เรียงต่อกันในไฟล์ (แต่ละอันเป็น linear chain เดียวไหลบนลงล่าง ไม่แตกกิ่งขนานกันในอันเดียว) วิธีนี้แก้ปัญหาล้นจอได้โดยไม่ต้องเสียเนื้อหา
- โครงสร้างเนื้อหา: Symptom (บนสุด, เขียนเป็น text ธรรมดานอกแผนภาพก็ได้ถ้ามีแค่ประเด็นเดียวที่แตกไปหลายกิ่ง) → ประเด็นหลัก (เป็นแผนภาพย่อย) → evidence/observation → root cause → action ที่ต้องทำ

## 5. สรุป Root Cause
เขียนเป็น numbered/bullet list สั้นๆ ก่อนแผนภาพ (จับใจความสำคัญ 2-4 ข้อ อ้างอิงตัวเลขที่คำนวณได้) แล้วค่อยตามด้วยแผนภาพ — Thada ต้องการทั้งสองแบบคู่กัน (text สรุป + visual)

## 6. อัปเดต hub note และ daily log
เหมือน [[spc-pdf-note]] §6 — เพิ่ม wikilink ใน `SPC Home.md` (ทั้งสองที่) และอัปเดต `notes\daily\YYYY-MM-DD.md` (+ mirror)

## หมายเหตุสภาพแวดล้อม / Excel COM gotchas (เจอมาแล้วจริง เสียเวลาไปเยอะ)

- **ไม่มี python/openpyxl/pandas/ImportExcel** — ใช้ Excel COM เท่านั้น
- **Orphan EXCEL.EXE process = ความเสี่ยง data loss จริง** — เคยเกิด: script error กลางคัน + force-kill process ทำให้ sheet ของ Thada หายจากไฟล์จริง (ไฟล์ยังไม่ได้ save แต่ process ค้างไป lock ไฟล์) กู้คืนได้จาก `%APPDATA%\Microsoft\Excel\<filename> (version 1).xlsb` (Excel AutoRecover snapshot) — **ต้อง `Get-Process EXCEL | Stop-Process -Force` + ลบไฟล์ `~$...xlsx` (lock file) ก่อนเปิดไฟล์ซ้ำทุกครั้ง โดยเฉพาะหลัง script error** ไม่ใช่แค่ตอนจบงาน
- **`Range.Value2 = <int>` throws `InvalidCastException`** ("Unable to cast object of type 'System.Int32' to type 'System.String'") — cast เป็น `[double]` เสมอก่อน assign ตัวเลขให้ Value2 (string ใช้ได้ปกติ)
- **`Range.Value2 = "=..."` (text ที่ขึ้นต้นด้วย `=`) throws COMException 0x800A03EC** — Excel พยายาม parse เป็นสูตร ห้ามให้ plain-text value ขึ้นต้นด้วย `=`
- **PowerShell variable name ไม่ case-sensitive** — อย่าใช้ `$n` และ `$N` (หรือชื่อคล้ายกันต่างแค่ case) ในขอบเขตเดียวกัน จะทับกันเงียบๆ ไม่ error แต่ผลลัพธ์ผิด (เจอมาแล้ว 2 ครั้งในการคำนวณ ANOVA loop)
- ปิด PowerShell script ทุกอันด้วยการ release COM object ให้ครบ (`Workbook`, `Worksheet`, `Range` ที่จับตัวแปรไว้, `Application`) + `[GC]::Collect()` + kill orphan process ท้ายสคริปต์เผื่อหลุด
