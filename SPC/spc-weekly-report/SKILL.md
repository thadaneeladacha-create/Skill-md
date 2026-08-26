---
name: spc-weekly-report
description: ใช้ skill นี้เมื่อ Thada ขอสรุป/อัพเดท action ของสัปดาห์นี้ หรือขอทำรายงานประจำสัปดาห์ส่งหัวหน้า — trigger เมื่อพูดถึง "อัพเดท action ของ week นี้", "ทำ weekly report", "ส่งรายงานหัวหน้า", "สรุปสัปดาห์นี้ให้หัวหน้า", "ทำ excel weekly เหมือน week ที่แล้ว" ครอบคลุมขั้นตอน: รวบรวม daily log ของสัปดาห์จาก vault Projects\Report\{year}\week-N-.../daily\ → สร้าง weekly summary note (.md) ใน Projects\Report\{year}\week-N-...\ (source of truth เดียว) → สร้างไฟล์ Excel รายงานรูปแบบเดียวกับสัปดาห์ก่อนหน้าใน X:\QM\IMS\Thada\Report\WeekN\
---

# SPC Weekly Report: Daily Logs → Weekly Summary → Excel Report ส่งหัวหน้า

ขั้นตอนมาตรฐานสำหรับสรุปงานประจำสัปดาห์ของ Thada (Quality/SPC Engineer ที่ HANA Microelectronics) จาก daily log ที่มีอยู่แล้ว แล้วส่งเป็นรายงาน Excel ให้หัวหน้าที่ `X:\QM\IMS\Thada\Report\WeekN\`

> **2026-08-11:** โครงสร้าง vault ปรับจาก `Projects/SPC/daily/` + `Projects/SPC/weekly/` (flat) เป็น `Projects/Report/{year}/week-N-YYYY-MM-DD-to-YYYY-MM-DD/daily/` (nested ตาม year → week → daily) เพราะ `daily/` เดิมกลายเป็น journal รวมข้ามหลายโปรเจกต์ (ไม่ใช่ SPC อย่างเดียว) เลยแยกออกมาให้ SPC มีโครงสร้างรายงานของตัวเองชัดเจน ไม่ปนกับโปรเจกต์อื่น

## ⚠️ กฎสำคัญ: ขอบเขตการเขียนบน X:\ (ห้ามละเมิดเด็ดขาด)

**`X:\` คือ network share ส่วนกลาง (server กลางของทั้งแผนก/บริษัท) ไม่ใช่พื้นที่ส่วนตัว**

**ห้ามเพิ่ม, ลบ, หรือแก้ไขไฟล์/โฟลเดอร์ใดๆ บน `X:\` ที่อยู่นอก `X:\QM\IMS\Thada\` เด็ดขาด** ไม่ว่ากรณีใดก็ตาม (แม้จะดูเกี่ยวข้องหรือเป็นการช่วยจัดระเบียบก็ตาม) เพราะไฟล์นอกโฟลเดอร์นี้เป็นของคนอื่น/ทีมอื่นที่ใช้ server เดียวกัน การแก้ไขผิดที่จะกระทบคนอื่นทันทีโดยไม่มีทางย้อนกลับง่ายๆ (ไม่ใช่ vault ของตัวเองที่มี git/backup)

- ✅ อ่าน (read-only) ไฟล์นอก `X:\QM\IMS\Thada\` ได้ ถ้าจำเป็นต้องอ้างอิง (เช่น เทียบ format กับทีมอื่น) — แต่ต้องขอ confirm จาก Thada ก่อนเสมอ ไม่ทำเองโดยไม่ถาม
- ❌ ห้าม write/delete/rename/move ใดๆ นอก `X:\QM\IMS\Thada\` โดยเด็ดขาด
- ภายใน `X:\QM\IMS\Thada\` เองก็ให้ระวัง — แก้ไข/ลบเฉพาะไฟล์ที่เกี่ยวกับ weekly report ของสัปดาห์ที่กำลังทำเท่านั้น อย่าไปแตะ WeekN-1, WeekN-2 ฯลฯ ของสัปดาห์ก่อนๆ โดยไม่ได้รับการร้องขอ

## 0. เช็ค convention ที่มีอยู่ก่อนเสมอ

1. อ่าน daily log ทั้งหมดของสัปดาห์นี้จาก vault `Projects\Report\{year}\week-N-YYYY-MM-DD-to-YYYY-MM-DD\daily\` (source of truth เดียว — โครงสร้างนี้ปรับจาก `Projects\SPC\daily\` เดิมมาเมื่อ 2026-08-11, ดู [[Report/2026/_Index]] สำหรับ index ของทุก week ในปีนั้น) — ถ้าโฟลเดอร์ของสัปดาห์นี้ยังไม่มี ให้สร้างตาม pattern เดียวกับสัปดาห์ก่อนๆ (`week-N-YYYY-MM-DD-to-YYYY-MM-DD/daily/`)
2. เช็คว่าสัปดาห์ที่แล้วมีไฟล์ Excel ตัวอย่างอยู่ไหมที่ `X:\QM\IMS\Thada\Report\WeekN-1\*.xlsx` — **ต้องใช้รูปแบบเดียวกันทุกครั้ง** (ชื่อไฟล์, sheet name, column headers, การจัดฟอร์แมต) อ่านโครงสร้างไฟล์เก่าด้วย Excel COM ก่อนสร้างไฟล์ใหม่เสมอ อย่าเดา format เอง
3. หา week number ปัจจุบัน — นับจากโฟลเดอร์ WeekN ที่มีอยู่ใน `X:\QM\IMS\Thada\Report\` (WeekN ล่าสุด + 1) ไม่ใช่นับจากปฏิทินเอง — เลข week นี้ต้องตรงกับเลข week ที่ใช้ตั้งชื่อโฟลเดอร์ฝั่ง vault ด้วย (`week-N-...`)

**⚠️ วัน-วันที่ ต้องยืนยันจาก daily log เสมอ (บทเรียน 2026-07-17):** อย่าเดา mapping วัน↔วันที่เอง — daily log แต่ละไฟล์ระบุวันในบรรทัด "บริบท" อยู่แล้ว (เช่น `2026-07-13.md` = "วันจันทร์", `2026-07-14.md` = "วันอังคาร") ให้อ่านยืนยันทุกวัน สัปดาห์ทำงานคือ **จันทร์–ศุกร์** (5 วัน) — เช็คว่าเก็บ daily log ครบตั้งแต่วันจันทร์จริงของสัปดาห์นั้น (เช่น week ที่จบวันศุกร์ 07-17 ต้องเริ่มวันจันทร์ 07-13 **ไม่ใช่ 07-14**) รอบแรกเคยพลาด: เลื่อนวันไปหมด (ใส่ Mon=07-14), ตกวันจันทร์ 07-13 ทั้งวัน, และใส่วันปลอม Fri 07-18 ที่ไม่มี log — Thada จับได้ ต้องแก้ทั้ง Excel + summary note + README ใหม่หมด

## 1. รวบรวมเนื้อหาจาก Daily Log

อ่าน daily log ทุกวันของสัปดาห์นั้น (จันทร์–ศุกร์ หรือเท่าที่มี) จาก `Projects/Report/{year}/week-N-YYYY-MM-DD-to-YYYY-MM-DD/daily/YYYY-MM-DD.md` แล้วสรุปเป็นหัวข้อ:
- งานหลักที่ทำแต่ละวัน (แยกตามวัน)
- ผลลัพธ์/ตัวเลขสำคัญ (เช่น ANOVA F/P-value, %GRR, metrics อื่นๆ)
- Root cause / findings ที่เจอ
- Action items พร้อม owner + due date + status
- งานค้าง/next steps

## 2. สร้าง Weekly Summary Note (.md)

สร้างไฟล์ `Projects/Report/{year}/week-N-YYYY-MM-DD-to-YYYY-MM-DD/week-N-YYYY-MM-DD-to-YYYY-MM-DD.md` ใน vault (source of truth เดียว — ดู §4 sync สำหรับ external report):
- Executive summary
- Daily breakdown (วันต่อวัน)
- ตารางผลลัพธ์/metrics สำคัญ
- ตาราง action items (No./Action/Owner/Due/Priority/Status)
- Next week plan
- Links กลับไป daily log, meeting notes, investigation notes ที่เกี่ยวข้อง

อัพเดท `SPC Home.md` เพิ่มลิงก์ section "Weekly Summary" ด้วยทุกครั้งที่สร้าง weekly note ใหม่

## 3. สร้างไฟล์ Excel รายงาน (รูปแบบเดียวกับสัปดาห์ก่อน)

เครื่องนี้ไม่มี python/openpyxl — ใช้ Excel COM automation:

```powershell
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$workbook = $excel.Workbooks.Add()
$ws = $workbook.Sheets(1)
$ws.Name = "Thada"   # ชื่อ sheet เดิมตาม week ก่อนหน้า — เช็คให้ตรง
```

**โครงสร้างมาตรฐาน (อ้างอิงจาก Week1/Week2 format — เช็คของจริงจากไฟล์ก่อนหน้าเสมอ):**
- Row 1: Title `"Training Report - Week N (WWXX)"` + วันที่อัพเดทใน column ท้ายๆ
- Row 3: Header — `WW | Day | Date | Activity | Summary | Instructor | Training Method | Assigned tasks | Status of Assigned Tasks | Remark`
- Row 4 เป็นต้นไป: ข้อมูลรายวัน (1 แถวต่อ 1 กิจกรรม, วันเดียวกันมีได้หลายแถว โดยเว้น Day/Date ซ้ำเป็นค่าว่าง)
- ใช้ `WrapText = $true` และตั้ง `RowHeight` ให้พออ่านง่าย (~60pt)
- Column widths: Summary column กว้างสุด (~45), Activity/Remark รองลงมา

**⚠️ Visual style ต้องตรงกับสัปดาห์ก่อนหน้าเป๊ะ (สี, ตำแหน่ง text, alignment) — decoded จาก Week6 ด้วย Excel COM 2026-08-21, ยืนยันกับ Thada แล้ว:**

ห้ามเดาสีจาก `.Interior.Color`/`.Font.Color` ตรงๆ (เป็น OLE BGR-packed int อ่านตาไม่ออก) ให้ decode ด้วย:
```powershell
Add-Type -AssemblyName System.Drawing
[System.Drawing.ColorTranslator]::FromOle($colorValue)   # -> ได้ R/G/B จริง
[System.Drawing.ColorTranslator]::ToOle($rgbColor)        # -> แปลงกลับตอนเขียนค่า
```

สี/ตำแหน่งมาตรฐาน (ใช้ script อ้างอิง `scripts/build-weekly-excel-template.ps1` เป็นจุดเริ่ม ไม่ใช่รันเฉยๆ โดยไม่ปรับ):

| องค์ประกอบ | สี/ตำแหน่ง |
|---|---|
| Font | Calibri ทั้งไฟล์ (body 11pt, title 14pt bold) |
| Title (A1) | ตัวอักษรสี NAVY `#002060`, bold, 14pt, พื้นขาว |
| Update badge (H1, เช่น "Update: 21 Aug 2026") | ตัวอักษรขาวตัวหนา บนพื้น CORAL `#F23A73`, จัดกลาง |
| Header row (row 3) | ตัวอักษรขาวตัวหนา บนพื้น NAVY `#002060`, จัดกลางทั้งแนวนอน-แนวตั้ง |
| Data rows — ทุกคอลัมน์ ยกเว้น Summary | จัดกลางทั้งแนวนอน-แนวตั้ง |
| Summary column (E) | จัดชิดซ้าย-บน (ไม่ใช่กลาง), **ตัวอักษรสี NAVY** `#002060` (ไม่ใช่ดำ) |
| WW column (A) | **merge cell ข้ามทุกแถวข้อมูลของสัปดาห์นั้น** (เช่น `A4:A8`) เป็นค่าเดียว `"WW34"` จัดกลาง — ไม่ใช่แยกทีละแถว |
| Status column (I) fill | `Completed` → GREEN `#A9D08E`, `In-progress` → GOLD `#FFE699`, ว่าง/holiday → ไม่ต้องเติม (ดูแถว holiday ด้านล่าง) |
| Border | **ไม่มี** cell border ชัดเจน — อาศัย Excel gridlines ปกติ (`DisplayGridlines = True`) เท่านั้น อย่าใส่ border เพิ่มเอง |
| แถว holiday (ถ้ามีวันหยุดในสัปดาห์) | ทั้งแถว (col C ถึง J) fill NAVY `#002060` + ตัวอักษรขาวตัวหนา, ใส่คำว่า `"Holiday"` ในคอลัมน์ Date, col A/B (WW/Day) ไม่ fill — ดูตัวอย่างจริงที่ Week6 แถว Wed 08-12 |

ก่อนเริ่มสร้างไฟล์ใหม่ทุกครั้ง แนะนำให้ decode สีจากไฟล์ WeekN-1 จริงอีกครั้งด้วย snippet ด้านบน เผื่อ Thada เปลี่ยน branding — อย่า hardcode ค่าจากตารางนี้แบบไม่เช็คซ้ำถ้าเป็นไปได้

**⚠️ Summary column: bullet point สั้น ไม่ใช่ paragraph เทคนิค (ยืนยันกับ Thada 2026-08-07):** หัวหน้าไม่ต้องการรายละเอียดเทคนิคเชิงลึก (ชื่อ script, ADR number, COM automation quirk, % ตัวเลขละเอียด) ต้องการแค่ "ทำอะไร → ได้อะไร" แบบ bullet สั้นๆ อ่านเร็ว:
- เขียนแต่ละ bullet ด้วย bullet character `[char]8226` (•) คั่นด้วย `[char]10` (newline ภายใน cell เดียวกัน) ไม่ใช่ paragraph ยาวแบบ prose
- ตัดศัพท์เทคนิคเฉพาะทาง (ชื่อไฟล์ script, ADR-XXXX, ชื่อฟังก์ชัน/ตัวแปรโค้ด, COM/VBA quirk) ออก เหลือแค่ผลลัพธ์ทางธุรกิจ/โปรเจค
- ตัวเลขสำคัญ (metric หลักที่ตัดสินใจได้ เช่น "one method clearly performs best") เก็บไว้ได้ แต่ไม่ต้องละเอียดทุกทศนิยม
- รายละเอียดเทคนิคเต็มให้ไปอยู่ใน Remark column link (PDF ของ daily log) แทน — ดูหัวข้อถัดไป

**⚠️ Remark column: hyperlink ไปยัง PDF ของ daily log แต่ละวัน (ยืนยันกับ Thada 2026-08-07):** ทำตาม pattern เดิมที่เจอใน Week4 (`$J$7 -> 2026-07-30.pdf`, `$J$8 -> 2026-07-31.pdf` ข้อความ `"For more detail please follow link :"`) — ให้ทำ**ทุกวัน** (ไม่ใช่แค่บางวัน):

1. Convert daily log แต่ละวัน (`Projects\Report\{year}\week-N-.../daily\YYYY-MM-DD.md`) เป็น PDF ด้วย **Word COM automation** (`scripts/md-to-pdf.ps1` ในสกิลนี้ — bundled แล้ว ไม่ต้องเขียนใหม่):
   ```powershell
   powershell.exe -File "<skill-dir>\scripts\md-to-pdf.ps1" `
     -MdPath "D:\Obsidian\Thadaverse\Projects\Report\2026\week-5-2026-08-03-to-08-07\daily\2026-08-07.md" `
     -PdfPath "X:\QM\IMS\Thada\Report\WeekN\2026-08-07.pdf" `
     -TitleText "Daily Log - Fri 07-Aug-2026"
   ```
   Script อ่าน `.md` ตรงจาก vault ด้วย `Get-Content -Encoding UTF8` (ไม่ inline ภาษาไทยใน `.ps1` — กัน mojibake ตาม encoding gotcha เดิม), แปลง markdown heading/bullet/checkbox/table เป็น Word style คร่าวๆ แล้ว export เป็น PDF ด้วย `Document.ExportAsFixedFormat(path, 17)` (17 = `wdExportFormatPDF`)
2. ตั้งชื่อไฟล์ PDF ตามวันที่ (`YYYY-MM-DD.pdf`) วางไว้โฟลเดอร์เดียวกับ Excel (`X:\QM\IMS\Thada\Report\WeekN\`)
3. ใส่ hyperlink ในเซลล์ Remark ของแต่ละแถว ด้วย `Worksheet.Hyperlinks.Add(cell, address, subaddress, screentip, textToDisplay)` — `address` เป็น relative filename เฉยๆ (เช่น `"2026-08-07.pdf"`) ไม่ใช่ full path เพราะไฟล์อยู่โฟลเดอร์เดียวกัน, `textToDisplay` = `"For more detail please follow link :"` (ข้อความเดิมทุกครั้ง ไม่เปลี่ยน)

**❌ ห้ามใช้ Edge/Chrome headless (`msedge --headless --print-to-pdf`) เพื่อแปลง PDF (บทเรียน 2026-08-07):** เคยลองแล้วค้าง (hang เกิน 120s) ต้อง `taskkill /F /IM msedge.exe` เพื่อเคลียร์ — คำสั่งนี้ฆ่า Edge process **ทั้งหมดในเครื่อง** รวมถึง browser session จริงของ Thada (มีถึง ~19 PID ที่ไม่เกี่ยวข้องโดนฆ่าไปด้วยรอบหนึ่ง) เป็นความเสี่ยงที่ยอมรับไม่ได้ **ใช้ Word COM (`ExportAsFixedFormat`) เท่านั้นสำหรับแปลง .md → PDF** ปลอดภัยกว่ามาก ไม่แตะ process อื่นของผู้ใช้เลย

**⚠️ ถ้าวันนั้นมีการเขียน how-to/hand-off guide ฉบับเต็มลง vault (เช่น `Projects/SPC/How to/*.md`) ให้ลิงก์ Remark ไปที่ guide แทน daily-log PDF ธรรมดา (ยืนยันกับ Thada 2026-08-21):**
- ใช้ `scripts/md-to-pdf-with-images.ps1` (ไม่ใช่ `md-to-pdf.ps1` ตัวธรรมดา) — ต่างกันตรงที่ตัวนี้ embed รูป `![alt](attachments/.../xxx.png)` เข้าไปในเอกสารจริง (ผ่าน `InlineShapes.AddPicture`) และข้าม ```mermaid``` code fence (Word render ไม่ได้) เพราะ guide พวกนี้มักมี screenshot ประกอบทุกขั้นตอนที่หัวหน้าควรเห็น ไม่ใช่แค่ข้อความ
  ```powershell
  powershell.exe -File "<skill-dir>\scripts\md-to-pdf-with-images.ps1" `
    -MdPath "D:\Obsidian\Thadaverse\Projects\SPC\How to\Require-Add-Spec-Guide.md" `
    -PdfPath "X:\QM\IMS\Thada\Report\WeekN\Require-Add-Spec-Guide.pdf" `
    -TitleText "Require Add Spec - Full Guide"
  ```
- ตั้งชื่อไฟล์ PDF ตามชื่อ guide note (ไม่ใช่ตามวันที่) วางไว้โฟลเดอร์เดียวกับ Excel
- Hyperlink ในแถวของวันนั้นชี้ไปไฟล์ guide PDF นี้แทน `YYYY-MM-DD.pdf` (ข้อความ `"For more detail please follow link :"` เหมือนเดิม)
- วันอื่นๆ ที่ไม่มี guide ฉบับเต็ม ยังคงลิงก์ไป daily-log PDF ตามปกติ (`md-to-pdf.ps1` ธรรมดา)
- ไฟล์ daily-log PDF ของวันนั้นจะไม่มีลิงก์ชี้ไปแล้ว แต่ไม่ต้องลบทิ้งอัตโนมัติ — ถามหรือรอ Thada สั่งก่อน (กฎ "ระวังใน `X:\QM\IMS\Thada\`" ด้านบน)

**Path:** `X:\QM\IMS\Thada\Report\WeekN\<ชื่อไฟล์เดียวกับ week ก่อนหน้า>.xlsx` (เช่น `ThadaN.090077.xlsx` — เช็คชื่อไฟล์จาก week ก่อนหน้าเสมอ อย่าเปลี่ยนชื่อเอง)

เพิ่มไฟล์เสริมถ้ามี (เช่น mind map HTML, README navigation guide, daily-log PDFs ตามหัวข้อข้างต้น) — ดูตัวอย่างจาก `X:\QM\IMS\Thada\Report\Week2\` ว่ามีไฟล์อะไรบ้าง

**⚠️ ก่อน copy ไฟล์ HTML/report ใดๆ ไป server กลาง `X:\` ต้องเช็ค asset embedding เสมอ (บทเรียน 2026-07-17):** `X:\QM\IMS\...` เป็น network share ที่คนอื่นเปิดดู — ถ้าไฟล์ HTML อ้างอิงรูป/CSS/JS ผ่าน path ในเครื่อง local (`D:\...`, `file://`, relative path ไปโฟลเดอร์ที่ไม่ได้ copy ไปด้วย) คนอื่นจะเห็นรูปแตก/ไฟล์พัง ก่อน copy ให้ verify ว่าไฟล์ **self-contained**:
```bash
grep -oE '(src|href)="[^"]*"' file.html          # ต้องไม่มี D:\ / file:// / path local
grep -c 'data:image/[a-z]*;base64' file.html      # รูปควรฝังเป็น base64 (>0 = ฝังในตัว OK)
grep -oE '<script[^>]*src="[^"]*"' file.html       # ระวัง CDN JS ที่ต้องพึ่ง internet
```
mind map ที่ generate จาก skill `spc-pdf-note`/`spc-abnormality-note` ปกติฝังรูปเป็น base64 อยู่แล้ว (self-contained) — แต่ต้อง verify ทุกครั้งก่อนส่ง ไม่ assume

**ปิด Excel ให้ถูกวิธีเสมอ** (กัน orphan process):
```powershell
$workbook.SaveAs($outputFile)
$workbook.Close($false)
$excel.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($excel) | Out-Null
```
เช่นเดียวกัน ปิด Word ให้ถูกวิธีทุกครั้งหลังรัน `md-to-pdf.ps1` (script จัดการปิดให้อัตโนมัติอยู่แล้วในตัวสคริปต์ แต่ถ้าเขียน COM เพิ่มเองให้ตามแพทเทิร์นเดียวกัน: `$doc.Close($false)` → `$word.Quit()` → `ReleaseComObject`)

**ตรวจ orphan process หลังรัน COM ทุกครั้ง** (ไม่ใช่แค่ตอนจบงาน) — `Get-Process EXCEL`/`Get-Process WINWORD` แล้วดู `MainWindowTitle`: ถ้าว่างเปล่า = invisible instance ที่สคริปต์เราสร้าง ฆ่าทิ้งได้ปลอดภัยด้วย `Stop-Process -Id <id> -Force`; ถ้ามี `MainWindowTitle` (เช่นไฟล์ที่ Thada เปิดค้างอยู่จริง) **ห้ามฆ่า** เด็ดขาด

**⚠️ COM loop type-casting bug (เจอซ้ำหลายรอบ):** เขียนค่าหลายชนิด (string/int/double) ลง property เดียวกัน (เช่น `ColumnWidth`, cell value) ผ่าน `for` loop จาก array แบบ mixed-type จะโดน `InvalidCastException`/`COMException` แบบสุ่ม — แก้โดยแยกแต่ละค่าให้เขียนผ่านบรรทัดคำสั่งของตัวเอง (ไม่ loop) เช่น:
```powershell
# ❌ อย่าทำแบบนี้
for ($c=1; $c -le 10; $c++) { $ws.Columns.Item($c).ColumnWidth = $widths[$c-1] }
# ✅ แยกบรรทัด
$ws.Columns.Item(1).ColumnWidth = 34.14
$ws.Columns.Item(2).ColumnWidth = 11.43
# ...
```

## 4. Sync 2 ทาง (บังคับทุกครั้ง — ห้ามลืม)

หลังสร้าง/แก้ weekly summary note ต้อง sync ให้ครบทั้ง 2 ที่ในเทิร์นเดียวกัน:

1. **Vault:** `Projects/Report/{year}/week-N-.../week-N-....md` (source of truth เดียวสำหรับ .md — ไม่ mirror เข้า `D:\SPC\notes\` อีกต่อไป)
2. **External report:** `X:\QM\IMS\Thada\Report\WeekN\` (Excel + summary .md + supporting files — ตามกฎขอบเขต X:\ ด้านบน)

ถ้าอัพเดท `SPC Home.md` ในวอลต์ (เพิ่มลิงก์ weekly ใหม่) แก้ที่วอลต์ที่เดียวพอ

> เดิม skill นี้เคย mirror .md เข้า `D:\SPC\notes\` ด้วย (3-way sync) — เลิกใช้แล้วตามที่ Thada ตัดสินใจ (2026-08-04) ให้ vault เป็น source of truth เดียว ลด sync drift ส่วนไฟล์ที่มีอยู่เดิมใน `D:\SPC\notes\weekly\` จากรอบก่อนยังไม่ได้ลบ ทิ้งไว้เป็น legacy จนกว่า Thada จะสั่งเคลียร์

## 5. Checklist ก่อนแจ้งว่าเสร็จ

- [ ] **ไม่ได้เพิ่ม/ลบ/แก้ไขไฟล์ใดๆ บน `X:\` นอกเหนือจาก `X:\QM\IMS\Thada\`** (กฎสำคัญด้านบน — เช็คทุกครั้ง)
- [ ] อ่าน daily log ครบทุกวันของสัปดาห์
- [ ] weekly summary note สร้างครบทั้ง 2 ที่ (vault / external report ถ้าจำเป็น)
- [ ] SPC Home.md อัปเดตในวอลต์ ถ้ามีการแก้ไข
- [ ] Excel รายงานสร้างตามรูปแบบเดียวกับสัปดาห์ก่อนหน้า (เช็คชื่อไฟล์/sheet/header จริงจากไฟล์เก่า ไม่เดา)
- [ ] **Summary column เป็น bullet point สั้น ไม่ใช่ paragraph เทคนิค** (ตัด script name/ADR number/COM quirk ออก)
- [ ] **Remark column มี hyperlink ไปยัง daily-log PDF ของทุกวัน** (`scripts/md-to-pdf.ps1` + `Hyperlinks.Add`, ข้อความ `"For more detail please follow link :"`)
- [ ] **ไม่ได้ใช้ Edge/Chrome headless หรือ `taskkill /IM msedge.exe`** สำหรับแปลง PDF — ใช้ Word COM เท่านั้น
- [ ] Excel/Word ปิด COM object สะอาด ไม่มี orphan process/lock file ค้าง (เช็ค `MainWindowTitle` ก่อนฆ่า process ใดๆ)
- [ ] ไฟล์เสริม (mind map, README, daily-log PDFs) copy ตามความเหมาะสม
- [ ] **สี/alignment ของ Excel ตรงกับ WeekN-1 เป๊ะ** (title/header navy, update-badge coral, status สีตาม Completed/In-progress, WW column merge ข้ามแถว, Summary ชิดซ้าย-บนสีนาวี) — decode สีจริงด้วย `[System.Drawing.ColorTranslator]::FromOle()` ก่อนเทียบ ไม่เดาด้วยตา
- [ ] วันที่มี guide ฉบับเต็ม (how-to/hand-off) ลิงก์ Remark ไปที่ guide PDF (ผ่าน `md-to-pdf-with-images.ps1`) แทน daily-log PDF ธรรมดา
