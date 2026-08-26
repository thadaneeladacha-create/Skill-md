---
name: control-chart-macro
description: ใช้ skill นี้เมื่อ Thada ทำงานต่อโปรเจค Control Chart Calculator ใน D:\Macro — Excel/VBA tool ที่ browse raw data แล้วคำนวณ control limits (Xbar-R, Xbar-S, Xbar-MR) แสดงผลใน UserForm — trigger เมื่อพูดถึง "SPC Calc.xlsm", "D:\Macro", "UserForm1", "Module2", "control chart macro", "x-mr chart", "แก้ VBA control chart", หรือถามเรื่องไฟล์ใน D:\Macro
---

# Control Chart Calculator (D:\Macro)

Excel/VBA tool: user browse ไฟล์ raw data (.xls/.xlsx/.xlsm) → `UserForm1` เรียก `Module2` คำนวณ control limits → แสดงผลในกล่องบนฟอร์ม รองรับ 3 chart type: Xbar-R, Xbar-S, Xbar-MR (individuals).

## ไฟล์ที่เกี่ยวข้อง

- `D:\Macro\SPC Calc.xlsm` — **ตัวจริง** ที่มี live VBA project (UserForm1, Module2, sheets ต่างๆ)
- `D:\Macro\SPC Calc.backup.xlsm` — backup ก่อนแก้ VBA ครั้งแรก (2026-08-03) เก็บไว้เผื่อ revert
- `D:\Macro\PIXART-PAW3955 MASTER AMWL.xlsx` — ตัวอย่าง raw data (ห้ามแก้ — tool ต้องเปิด read-only เสมอ)
- `D:\Macro\UserForm1.frm`/`.frx`, `D:\Macro\Module2.bas` — **stale exports เก่า อยู่นอก .xlsm** แก้ไฟล์พวกนี้ตรงๆ **ไม่มีผล** กับตัวจริง (ดู "แก้ VBA ยังไง" ด้านล่าง)
- `D:\Macro\CONTEXT.md` — glossary ของโปรเจคนี้ (chart type, subgroup row, dispersion column, X source column, constants table ต่างๆ)
- `D:\Macro\docs\adr\0001-cache-loaded-data-for-recalc.md` — ADR: form cache ข้อมูลที่โหลดไว้ ไม่ re-open ไฟล์ทุกครั้งที่เปลี่ยน chart type
- `D:\Macro\docs\adr\0002-column-mapping-by-real-data-not-names.md` — ADR: การ map คอลัมน์แบบ real-data-not-names (**ยังใช้ได้กับ Xbar-R และ Xbar-MR's `avg_read / X` branch เท่านั้น** — Xbar-S ถูก revert แล้ว ดู ADR 0003)
- `D:\Macro\docs\adr\0003-xbar-s-reverts-to-name-matching.md` — ADR: **สำคัญมาก, ล่าสุด (2026-08-04)** Xbar-S (และ Xbar-MR branch ที่เลือก `sd / MR`) revert กลับไปใช้ name-matching mapping (`avg_read / X` = X̄, `sd / MR` = dispersion) อ่านก่อนแก้ logic การเลือกคอลัมน์ใน `CalculateChart`
- `D:\Obsidian\Thadaverse\Projects\Macro Project\_MOC.md` — **vault hub note** ของโปรเจคนี้ (สร้าง 2026-08-04, ตาม convention เดียวกับ `Projects/Automation/_MOC.md`) มี status table, ADR list, bug-fix table, next steps — **อัปเดตไฟล์นี้ทุกครั้งที่มีการเปลี่ยนแปลงสำคัญ** (ไม่ใช่แค่ memory file นี้) เพราะเป็นที่ที่ Thada อ่านจริง ลิงก์จาก `SPC Home.md` ส่วน Projects

**Thada แก้ VBA เองโดยตรงในนี้ได้เหมือนกัน** (ไม่ได้ผ่าน Claude เสมอไป) — ก่อนแก้อะไรเพิ่มควร re-read live code จาก `.xlsm` ก่อนทุกครั้ง (ดู "แก้ VBA ยังไง" ด้านล่าง) อย่าเชื่อ scratchpad `.bas` เก่าเป็นความจริงเด็ดขาด

## Architecture

**`Module2`** (standard module):
- `LoadDataFrame(dataWb As Workbook) As Object` — โหลดข้อมูลเป็น header→column dictionary (`Scripting.Dictionary`) โดย**รวมทุกชีทที่ชื่อขึ้นต้นด้วย `FileExportInprocess_Machine`** เข้าด้วยกัน (ดูหัวข้อ "หลายชีทซ้อนกัน" ด้านล่าง) ไม่ใช่แค่ชีทเดียว
- `CalculateChart(df As Object, chartType As String, [overrideE2], [overrideD3], [overrideD4], [mrSourceColumn As String = "sd / MR"], [skipEmptyFilenm As Boolean = False], [overrideN As Variant]) As ChartResult` — คำนวณตาม chart type, คืนค่าเป็น `ChartResult` (Public Type). `mrSourceColumn` ใช้เฉพาะ xbar-mr (ดูหัวข้อ "คอลัมน์ raw data ที่ใช้" ด้านล่าง). `skipEmptyFilenm` ผูกกับ `CheckBox1` ("Manual filter mode") ดูหัวข้อ "txtfilenm filter" ด้านล่าง. **`overrideN` เพิ่มใหม่ 2026-08-04** — ถ้าส่งมาจะใช้แทน `df("sample_size")(1)` ตอน lookup ค่าคงที่ (มีผลกับ Xbar-R/Xbar-S เท่านั้น, Xbar-MR ใช้ `X-MR Chart Constants` หรือ `overrideE2/D3/D4` แทนอยู่แล้ว ไม่แตะ `subg`) ผูกกับ `TextBox1` ที่แก้ไขได้แล้ว ส่งเข้า `CalculateChart` เมื่อกด `CommandButton2` ("Recalculate") — **`subg = CDbl(overrideN)` ต้อง cast เสมอ** (แก้บั๊กจริงที่ Thada เจอ: `TextBox.Value` เป็น `String` เสมอ ส่ง string ตรงๆเข้า `Match()` กับคอลัมน์ตัวเลขใน constants table แล้ว match ไม่เจอ ทำให้ error แล้วโดน `On Error GoTo Fail` ดักเงียบๆ กลายเป็น "คำนวณไม่สำเร็จ" — เหมือน pattern เดิมที่ `overrideE2/D3/D4` cast ด้วย `CDbl` อยู่แล้ว)

**`UserForm1`**: `ComboBox1` (xbar-R/xbar-S/xbar-MR), `TextBox1` (sample_size — **แก้ไขได้แล้วตั้งแต่ 2026-08-04**, ดูหัวข้อ "subgroup size (n) แก้ไขได้" ด้านล่าง), `CommandButton1` ("Browse"), `TextBox2-4` (constant1/2/3 — editable เฉพาะโหมด xbar-MR), `TextBox5-8` (LCL-X/UCL-X/UCL-R/LCL-R, แสดงทศนิยม **5 ตำแหน่ง** ตั้งแต่ 2026-08-04), `Label1-3` (ชื่อ constant, เปลี่ยนตาม chart type: A2/D3/D4, A3/B3/B4, E2/D3/D4), `Label6-7` (UCL-R/LCL-R ↔ UCL-S/LCL-S ↔ UCL-MR/LCL-MR), `CommandButton2` ("Recalculate" — **แสดงทุก chart type ตั้งแต่ 2026-08-04** (เดิมโผล่เฉพาะ xbar-MR), ใช้ตอนแก้ constants/MR source (xbar-mr) หรือแก้ `TextBox1` (n) แล้วอยากให้คำนวณใหม่ (ทุก chart type)), `ComboBox2`+`Label11` ("MR from:" — โผล่เฉพาะโหมด xbar-mr, เลือกว่าจะเอา MR จากคอลัมน์ `sd / MR` หรือ `avg_read / X`), `Label12`+`ListBoxConstants` (ตาราง reference ของ `Constants Table (n=2-50)` ทั้งชุด n=2..50 แสดงบนฟอร์มตลอด ไม่ผูกกับ chart type — ดู "ตาราง Constants Table บนฟอร์ม" ด้านล่าง), `CheckBox1` ("Manual filter mode" — toggle เดียว, ไม่ใช่ multi-select แล้ว, ดูหัวข้อ "txtfilenm filter" ด้านล่าง — `Label13`/`ListBox2` เดิมถูกถอดออกไปตอน 2026-08-04 รอบสอง อย่าอ้างอิงถึงอีก), `m_df`/`m_loaded` (module-level cache — Browse ครั้งเดียว, เปลี่ยน ComboBox1/ComboBox2/CheckBox1 แล้ว recalc จาก cache ไม่ re-open ไฟล์)

### subgroup size (n) แก้ไขได้

`TextBox1` เดิม (ก่อน 2026-08-04) แค่ *แสดง* `sample_size` จากข้อมูลหลัง Browse (`Me.TextBox1.Value = m_df("sample_size")(1)`) แต่ไม่เคยถูกอ่านกลับเข้าไปคำนวณเลย — แก้ค่าในกล่องแล้วไม่มีผลอะไร ตอนนี้แก้ไขได้จริง: `ApplyChartTypeUI` set `CommandButton2.Visible = True` เสมอ (ทุก chart type ไม่ใช่แค่ xbar-mr แล้ว), กด `CommandButton2` → `RunCalculation True` → ส่ง `overrideN:=Me.TextBox1.Value` เข้า `CalculateChart` (ทั้ง branch xbar-mr และ branch อื่นๆ) แทนที่จะ derive `subg` จาก `df("sample_size")(1)` ปกติ — มีผลกับการ lookup constants (`Constants Table (n=2-50)`) เฉพาะ Xbar-R/Xbar-S เท่านั้น (Xbar-MR ไม่ใช้ `subg`)

**หมายเหตุ layout:** Thada ปรับ position/size ของทุก control เองหมดแล้วตั้งแต่ 2026-08-04 (form โตขึ้นมากจาก 545x334 เดิมเป็น ~993x394+) — เลขตำแหน่ง (`Left`/`Top`) ที่เขียนไว้ใน skill นี้เป็นแค่ตอนที่เพิ่ง `Controls.Add` เท่านั้น **ไม่ตรงกับตำแหน่งจริงปัจจุบันแล้ว** ถ้าจะเพิ่ม control ใหม่ ให้ query ตำแหน่งปัจจุบันจริงก่อนเสมอ อย่าอ้างอิงเลขจาก skill นี้ตรงๆ

### txtfilenm filter (on/off toggle)

**แก้ล่าสุด 2026-08-04 (รอบสอง):** `CheckBox1` ("Manual filter mode") — toggle เดียว ไม่ใช่ multi-select `ListBox2` แล้ว (ของเก่าถูกถอดออก, `PopulateFilterList`/`BuildFilterSet` ไม่มีในโค้ดแล้ว) ค่า default **unchecked = OFF** = คำนวณทุกแถวรวมถึงแถวที่ `txtfilenm` ว่าง, checked = ON = ข้ามแถวที่ `txtfilenm` ว่าง (พฤติกรรมแบบเดิมก่อนมี toggle) `CheckBox1_Change` trigger recalc ทันที ส่งเป็น `skipEmptyFilenm As Boolean` เข้า `CalculateChart` ทุกครั้งที่ `RunCalculation` เรียก ไม่ว่า chart type ไหน — ส่วน numeric-validity guard (ข้ามแถวที่ X/dispersion ว่างหรือไม่ใช่ตัวเลข) ทำงานเสมอไม่ผูกกับ toggle นี้

### ตาราง Constants Table บนฟอร์ม

`ListBoxConstants` เป็น native MSForms ListBox แบบหลายคอลัมน์ (ไม่ใช่ ActiveX grid แยกต่างหาก) ผูกกับข้อมูลผ่าน `RowSource = "'Constants Table (n=2-50)'!A5:J53"` + `ColumnHeads = True` (แถว header ดึงจากแถวเหนือ RowSource คือ row4 อัตโนมัติ) + `ColumnCount = 10` — วิธีนี้ **ไม่ต้อง copy ข้อมูลเข้า .List array เอง** แค่ตั้งค่า RowSource ก็พอ และจะ sync กับ sheet เองถ้ามีคนแก้ค่าคงที่ในชีทภายหลัง เนื่องจากฟอร์มเดิมสูงไม่พอ (`InsideHeight` แก้ผ่าน COM designer โดยตรงไม่ได้ — property ไม่ยอมให้ set จากภายนอก) ตอนแรกเพิ่ม `Me.Height = 620` ใน `UserForm_Initialize` เพื่อ resize ตอน runtime — **แต่ Thada แก้ไขปรับขนาดฟอร์มเองใน VBA IDE (F4 Properties) แล้วพบว่าไม่ติด เพราะโค้ดนี้ทับค่าที่ตั้งเองทุกครั้งที่ฟอร์ม initialize** จึง**ลบบรรทัด `Me.Height = 620` ออกแล้ว (2026-08-03)** ให้ Thada ปรับขนาดฟอร์มเองผ่าน Properties window ได้อิสระ — **ข้อควรระวัง:** ตอนนี้ Designer `InsideHeight` เดิม (334.5) ยังเตี้ยกว่าตำแหน่งที่ `ListBoxConstants` วางไว้ (top=358, สูงถึง ~537) ถ้า Thada ยังไม่ได้ปรับความสูงฟอร์มเองผ่าน Properties window ตารางจะโดนตัดขอบมองไม่เห็นเวลาเปิดฟอร์มจริง — ต้องปรับ Height ของ UserForm1 (ไม่ใช่ปรับที่ code) ให้พอเองอย่างน้อย ~560-620pt

### หลายชีทซ้อนกัน (repeated downloads)

Thada พบว่า download ข้อมูลจากระบบต้นทางซ้ำหลายครั้งเข้า workbook เดียวกันทำให้เกิดชีทซ้อน: `FileExportInprocess_Machine`, `FileExportInprocess_Machine(1)`, `FileExportInprocess_Machine (2)`, ... (Excel ตั้งชื่อกันชนแบบนี้เองเวลา copy/import ซ้ำ — บางครั้งมีวรรคหน้าวงเล็บ บางครั้งไม่มี) โค้ดเดิมอ่านแค่ชีทชื่อตรงเป๊ะเท่านั้น ทำให้ข้อมูลจากการ download ซ้ำๆหายไปเงียบๆ — **แก้แล้ว (2026-08-03):** `LoadDataFrame` วนหาทุกชีทที่ `Left(ws.Name, Len("FileExportInprocess_Machine")) = "FileExportInprocess_Machine"` (match แบบ prefix ไม่สน suffix) แล้วรวมแถวข้อมูลจากทุกชีทเข้า array เดียวกัน (เรียงตาม tab order) ก่อนคำนวณ — สมมติว่าทุกชีทมี header column เหมือนกัน (ใช้ header ของชีทแรกที่เจอเป็นหลัก) `CommandButton1_Click`'s `hasSheet` check ก็ใช้ prefix-match แบบเดียวกัน ทดสอบแล้วด้วย synthetic 3-sheet workbook (2+1+2 แถว → รวมถูกต้อง 5 แถว รวมถึง edge case ชีทที่มีข้อมูลแค่ 1 แถว)

## คอลัมน์ raw data ที่ใช้ (ชีท `FileExportInprocess_Machine`)

`chartType`, `sample_size`, `txtfilenm` (ตัวกรองว่าแถวว่างหรือไม่) — ส่วนคอลัมน์ที่เป็นตัวเลขจริงสำหรับคำนวณ ปัจจุบัน (2026-08-04, หลัง ADR 0003) **map ตรงกับชื่อคอลัมน์แบบ name-matching ทั้งหมด**:

| Chart Type | "X" (→ avgX / CL_X) | "Dispersion" (→ avgSecond / CL_R, คู่กับ constants) |
|---|---|---|
| Xbar-R | `avg_read / X` | `range_read` |
| Xbar-S | `avg_read / X` | `sd / MR` |
| Xbar-MR, `mrSourceColumn = "avg_read / X"` | `avg_read / X` | `range_read` |
| Xbar-MR, `mrSourceColumn = "sd / MR"` | `avg_read / X` | `sd / MR` |

**ประวัติ:** ก่อนหน้านี้ (2026-08-03, ADR 0002) เคยใช้ mapping ที่ไม่ตรงชื่อคอลัมน์ (Xbar-S ใช้ `range_read`=dispersion, `sd / MR`=X) เพราะตอนนั้น Thada ยืนยันจากข้อมูลจริงว่าชื่อคอลัมน์ไม่ตรงกับความหมายจริง — แต่ 2026-08-04 Thada ทบทวนสูตรอีกครั้ง (`UCL = X̄̄ + A3·S̄`) แล้วยืนยันตรงกันข้าม ว่า mapping แบบ name-matching (ตารางด้านบน) ถูกต้อง จึง revert กลับ (ADR 0003 supersede ADR 0002 สำหรับ Xbar-S และ Xbar-MR's `sd / MR` branch — ADR 0002 ยังใช้ได้กับ Xbar-R และ Xbar-MR's `avg_read / X` branch) **ห้าม "แก้กลับ" ไปมาระหว่างสอง mapping นี้อีกโดยไม่ได้รับการยืนยันจาก Thada ชัดเจน (อ่าน ADR 0002 + 0003 ให้ครบก่อน)**

หมายเหตุ: ไฟล์ตัวอย่าง `PIXART-PAW3955 MASTER AMWL.xlsx` มีแต่ record `chartType = "Xbar-R"` เท่านั้น — ไม่มีข้อมูล Xbar-S/Xbar-MR จริงให้เทียบ mapping ทั้งสองรอบเทสกับ synthetic data เท่านั้น (ดู session notes/git history สำหรับ debug harness ที่ใช้)

### mrSourceColumn parameter (xbar-mr เท่านั้น)

Record ที่ tag เป็น individuals/MR chart ไม่ได้เก็บค่า X (individual reading)/dispersion ไว้ที่คอลัมน์เดียวกันเสมอไป — ขึ้นกับว่า batch นั้น log ยังไง จึงให้ user เลือกเองผ่าน `ComboBox2` ("MR from:") ว่า batch นี้เป็น "แบบ R" หรือ "แบบ S" สูตรทั้งคู่ใช้ constant ชุดเดียวกันเสมอ (E2/D3/D4 — ไม่ใช่ A2/A3) มีแค่คอลัมน์ที่อ่านเปลี่ยนไป (**แก้ 2026-08-04 พร้อม ADR 0003** — เดิม dispersion เป็น `range_read` เสมอไม่ว่าเลือกอะไร ซึ่งผิดสำหรับ branch `sd / MR`):

- `mrSourceColumn = "avg_read / X"` (batch แบบ R): X̄̄ = `avg_read / X`, dispersion = `range_read` — เหมือน Xbar-R ทุกอย่าง
- `mrSourceColumn = "sd / MR"` (batch แบบ S): X̄̄ = `avg_read / X` (เหมือนเดิม), dispersion = `sd / MR` (**เปลี่ยนจาก `range_read`**) — เหมือน Xbar-S ทุกอย่าง ต่างแค่ constant เป็น E2 แทน A3

## Constants sheets

- `Constants Table (n=2-50)` — lookup ตาม `sample_size` (คอลัมน์ E-J: A2/D3/D4 สำหรับ Xbar-R, A3/B3/B4 สำหรับ Xbar-S) ใช้ได้เฉพาะ n=2..50
- `X-MR Chart Constants` — ค่าคงที่ fix ที่ n=2 เสมอ (E2=2.66, D3=0, D4=3.2665) ไม่ผ่าน `Constants Table` เพราะ sample_size ของ individuals chart มักเป็น 1

## แก้ VBA ยังไง (สำคัญ!)

**ห้ามแก้ `.frm`/`.bas` ตรงๆ** — ไฟล์พวกนั้น export แล้วไม่ sync กลับ ต้องแก้ผ่าน Excel COM automation (PowerShell) เข้า `.xlsm` โดยตรง:

```powershell
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false; $excel.DisplayAlerts = $false
$wb = $excel.Workbooks.Open("D:\Macro\SPC Calc.xlsm", $true, $false)  # $false=ไม่ readonly ตอนจะแก้

$mod = $wb.VBProject.VBComponents.Item("Module2").CodeModule
if ($mod.CountOfLines -gt 0) { $mod.DeleteLines(1, $mod.CountOfLines) }
$mod.AddFromString($newCode)   # $newCode = string จากไฟล์ .bas ที่เขียนไว้ใน scratchpad (อ่านด้วย ReadAllText UTF8)

# เพิ่ม control ใหม่บน UserForm designer
$designer = $wb.VBProject.VBComponents.Item("UserForm1").Designer
$btn = $designer.Controls.Add("Forms.CommandButton.1")

# ลบ component ทั้งตัว
$wb.VBProject.VBComponents.Remove($wb.VBProject.VBComponents.Item("Module1"))

$wb.Save()
$wb.Close($false); $excel.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
```

ก่อนแก้ครั้งแรกของ session ควร `cp "SPC Calc.xlsm" "SPC Calc.backup.xlsm"` ไว้ก่อนเสมอ (แก้ VBA ผ่าน COM ไม่มี undo, diff ยาก)

## Known gotchas

- **`Application.WorksheetFunction.Match` เทียบ text แบบ case-insensitive** — ถ้าชีท constants มีทั้ง "d3" (lowercase, เป็นค่า intermediate) และ "D3" (uppercase, ค่าที่ต้องการจริง) การ `Match("D3", ...)` จะไปเจอแถว "d3" ก่อนแล้วได้ค่าผิด ต้อง loop เทียบด้วย `StrComp(text, "D3", vbBinaryCompare) = 0` แทน (บั๊กนี้เจอจริงตอนทำ X-MR Chart Constants lookup)
- **`Application.Run` (COM late-binding) คืนค่า VBA `Type` (UDT) ไม่ได้** — error "Value does not fall within the expected range" เทส `CalculateChart` ที่ return `ChartResult` ตรงๆ ไม่ได้ วิธีเทส: เขียน temporary debug `Sub` ที่เรียกฟังก์ชันแล้ว dump ผลลงเซลล์ในชีทว่างๆ (เช่น `Workspace`) แล้วอ่านค่าเซลล์กลับมาแทน — **อย่าลืมลบ debug sub และ `.Clear()` เซลล์ก่อน save**
- **PowerShell: เรียก COM method โดยไม่ใส่ `()` เช่น `$ws.Cells.Clear` (ไม่ใช่ `$ws.Cells.Clear()`) จะไม่ทำงานจริง** — PowerShell แค่ print "OverloadDefinitions" กลับมาเฉยๆ ไม่ error แต่ก็ไม่ clear จริง (เจอเองตอน debug sheet `Workspace` ค้างข้อมูลทดสอบ)
- **`Application.Run` เรียก `Sub` (ไม่มี return value) บางครั้งค้าง (hang) แบบไม่ error ไม่ timeout ปกติ** — เจอตอน debug harness เป็น `Sub` ที่รับ string parameter หลายตัว, กด run แล้วค้างจน PowerShell timeout, ต้อง `taskkill /F` EXCEL.EXE ที่ค้างทิ้งก่อนลองใหม่ (เช็คด้วย `Get-Process EXCEL`) — เปลี่ยน debug harness จาก `Sub` เป็น `Function ... As String` ที่ return string ธรรมดาแทน แก้ปัญหาได้ (ไม่ได้ root-cause ชัดเจนว่าทำไม Sub ถึงค้าง แต่ Function คืนค่าง่ายๆ เสถียรกว่าเสมอ — ใช้ pattern นี้เป็นหลักเวลา debug ผ่าน COM)
- เปิดไฟล์ raw data ต้อง `Workbooks.Open(path, ReadOnly:=True)` และปิดด้วย `Close SaveChanges:=False` เสมอ — ของเดิม (ก่อนแก้) เคยเขียนทับ B1 แล้ว save ไฟล์ raw data โดยไม่ตั้งใจ
- **VBA editor auto-recase `.Rows` เป็น `.rowS` (ตัว S ใหญ่) ถ้ามีตัวแปร local ชื่อ `rowS` อยู่ในโมดูลเดียวกัน** — เจอใน `LoadDataFrame`/`CalculateChart` หลัง Thada แก้โค้ดเอง เป็นแค่เรื่อง casing ที่ VBA IDE auto-format ตาม identifier อื่นที่สะกดเหมือนกัน (case-insensitive) **ไม่ใช่บั๊ก** `.Rows` ยังอ้างถึง property `Worksheet.Rows` ตามปกติ แค่ดูแปลกตา อย่าไป "แก้" กลับเป็น `.Rows` เฉยๆ โดยไม่จำเป็น (ไม่มีผลอะไร)
- ชีท `Workspace` ในไฟล์เป็นชีทว่างเปล่า ไม่เกี่ยวกับ production code เลย — ใช้เป็น scratch area สำหรับ debug/test เท่านั้น
- **`Designer.Height`/`Designer.InsideHeight` set ผ่าน external COM automation ไม่ได้** ("property cannot be found" / "no overload") ทั้งที่อ่าน (get) ได้ปกติ — ถ้าต้องขยายฟอร์มให้สูง/กว้างขึ้น ให้ set `Me.Height`/`Me.Width` ใน VBA code เอง (เช่นใน `UserForm_Initialize`) แทน ซึ่ง set ได้ปกติตอน runtime — ส่วน control ใหม่ที่ตำแหน่ง Top/Left เกิน InsideHeight/InsideWidth เดิม ยัง `Controls.Add` ได้ปกติ ไม่ error แค่ต้อง resize ฟอร์มด้วย code ให้เห็นครบ
- **ตั้งค่า `.Font.Size` ผ่าน COM ทันทีหลัง `Controls.Add` บางทีพัง** ("Object reference not set...") — เป็น error ที่ไม่ fatal (script อื่นรันต่อได้ปกติ, save ผ่าน) แค่ข้าม step นั้นไปถ้าไม่จำเป็นต้องปรับ font
- **เทส UserForm โดยไม่ให้ popup ขึ้นจริง**: ใช้ `Load UserForm1` (ไม่ใช่ `.Show`) ใน debug `Function` ที่เรียกผ่าน `Application.Run` — `Load` จะ fire `UserForm_Initialize` และให้เข้าถึง property ของ control **public** ทุกตัว (เช่น `UserForm1.ListBoxConstants.List(0,0)`) ได้โดยไม่ต้องแสดงหน้าต่างจริง (ซึ่งจะ block/modal) จบแล้ว `Unload UserForm1` ทิ้ง
- **⚠️ ห้ามเรียก `Private Sub`/`Private Function` ของ `UserForm1` (เช่น `ApplyChartTypeUI`, `RunCalculation`, event handlers ทุกตัว) จาก debug module แยกต่างหาก** — สิ่งเหล่านี้ประกาศเป็น `Private` ทั้งหมด เข้าถึงจากนอกโมดูลไม่ได้ตามหลัก VBA พยายามเรียกแล้วทำให้ **Excel.exe ทั้ง process crash จริง** (`Application.Run` ล้มเหลวด้วย "The remote procedure call failed" HRESULT 0x800706BE แล้ว COM object ทั้งตัวตายตาม ทำให้ `.Save()`/`.Close()`/`.Quit()` ที่ตามมา error เป็น "RPC server is unavailable" ทั้งหมด) — เจอซ้ำ 2 ครั้งติดกันตอนพยายามเทส `CommandButton2.Visible` ทาง `UserForm1.ApplyChartTypeUI "xbar-R"` จาก module แยก **ข่าวดี:** ถ้า crash แบบนี้เกิดตอน `$wb.Save()` ยังไม่ทันรัน ไฟล์บน disk จะไม่ถูกแก้ (การแก้ทั้งหมดอยู่ใน memory ของ Excel session ที่ตายไปแล้ว) เช็คได้ด้วยการเปิดไฟล์ใหม่ (`ReadOnly:=True`) แล้ว list `VBComponents`/`CodeModule.Lines` ดู ถ้าไม่มี debug module ค้างอยู่และโค้ดที่ save ไว้ก่อนหน้ายังอยู่ครบ = ปลอดภัย **วิธีเทสพฤติกรรมที่ผูกกับ Private Sub แทน:** อ่านโค้ดตรงๆ ด้วยตาแทนการรันจริง (สำหรับ logic ง่ายๆ เช่น unconditional property assignment) หรือถ้าจำเป็นต้อง exercise จริง ให้ตั้งค่า public property ที่ trigger event ของมันเอง (เช่น set `ComboBox1.Value` เพื่อให้ `ComboBox1_Change` ทำงานเอง) แทนการเรียก Sub ตรงๆ — แต่ระวัง guard `If Not m_loaded Then Exit Sub` ที่ต้นเกือบทุก handler จะทำให้วิธีนี้ใช้ไม่ได้ถ้ายังไม่เคย Browse ไฟล์จริงมาก่อน (ต้อง set `m_df`/`m_loaded` เองไม่ได้เพราะเป็น `Private` เหมือนกัน — ทางเดียวที่เหลือคือ code review ตรงๆ)
- **เขียนข้อมูลลง Excel ผ่าน PowerShell COM ทีละเซลล์ (`$ws.Cells.Item(r,c).Value2 = x` ใน loop) บางทีพังแบบ "Unable to cast object of type ... to type 'System.String'" โดยไม่มีเหตุผลชัดเจน** — เจอตอนสร้าง synthetic test workbook หลายชีท วิธีแก้ที่เสถียรกว่า: เขียนทีละแถว โดย assign array 1 มิติเข้า Range 1 แถวหลายคอลัมน์ทีเดียว เช่น `$ws.Range("A2:F2").Value2 = [object[]]@("a",1,2,3,4,"b")` (ไม่ต้อง loop cell-by-cell) — ใช้ pattern นี้เป็นหลักเวลาต้องสร้างไฟล์ทดสอบผ่าน COM
- **⚠️ VBA `Or`/`And` ไม่ short-circuit (ไม่เหมือนภาษาอื่นๆ)** — ประเมิน operand ทั้งสองข้างเสมอ ห้ามเขียน `If (Not useFilter) Or someObject.Method(...) Then` โดยหวังว่าถ้า `useFilter=False` แล้ว `someObject.Method` จะไม่ถูกเรียก — VBA จะเรียกมันเสมอ ถ้า `someObject Is Nothing` จะ error 91 ทันที (บั๊กจริงที่เจอตอนเพิ่ม `filterSet.Exists(...)` ใน `CalculateChart` — กรณีไม่กรองอะไรเลย `filterSet` เป็น `Nothing` แต่โค้ดยังเรียก `.Exists` อยู่ดี ทำให้ error แล้วโดน `On Error GoTo Fail` ดักไว้เงียบๆ, `res.Success=False` โดยไม่มี error message ชัดเจน) วิธีแก้: แยกเป็น nested `If...Else` เพื่อ gate การเรียก method ไม่ให้ evaluate ฝั่งที่อาจ error เมื่อไม่จำเป็น
- **คำสั่ง COM read/write ธรรมดาๆ (แค่ `Workbooks.Open` + อ่าน property) บางทีค้างนาน 90-150+ วินาทีทั้งที่ไม่ error** — ไม่ใช่ hang จริงเสมอไป (ต่างจาก gotcha `Application.Run` เรียก `Sub` ค้างด้านบนซึ่ง hang จริงไม่จบ) เจอกับ background task ที่ `run_in_background`/timeout แล้วสุดท้าย**ทำงานจบสมบูรณ์เอง**ถ้ารอ ก่อน kill process ควรเช็ค `~$SPC Calc.xlsm` lock file ก่อน (ถ้ามี lock = Thada เปิดไฟล์ค้างอยู่ ต้องรอเขาปิด ไม่ใช่ปัญหาที่ script) และอ่าน background task output file ดูว่ามันคืบหน้าไปถึงไหนแล้วก่อนตัดสินใจ kill
- **`$excel.Quit()` + `ReleaseComObject` ใน PowerShell บางทีไม่ปิด `EXCEL.EXE` จริงๆ** — เจอ process ค้างอยู่จาก session read-only ก่อนหน้า (เปิด `.xlsm` ด้วย `ReadOnly:=True` เพื่อ dump code) ก่อนจะเขียนแก้ไฟล์ครั้งต่อไป ควรเช็คด้วย `Get-Process EXCEL` (หรือ `tasklist | grep EXCEL`) ก่อนเสมอ — **แต่ห้าม kill ทันที** ต้องเช็ค `~$SPC Calc.xlsm` lock file ก่อน (ตามข้อด้านบน): ถ้า**ไม่มี** lock file แปลว่า process ที่ค้างเป็นของ script เก่า ไม่ใช่ของ Thada เปิดอยู่ ปลอดภัยที่จะ `taskkill /F /IM EXCEL.EXE` ทิ้งก่อนเขียนต่อ ถ้า**มี** lock file ต้องรอ Thada ปิดไฟล์เอง
