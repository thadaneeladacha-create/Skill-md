---
name: form10-control-chart
description: ใช้ skill นี้เมื่อ Thada ทำงานเกี่ยวกับ HANA's Form 10 Rev A control chart build — เติมข้อมูล subgroup ที่คำนวณไว้แล้วลงในฟอร์ม `001_018_000026_Form_10_Rev_A_xlsx.xlsx` แล้วสร้าง native Excel Xbar-R chart ต่อท้าย — trigger เมื่อพูดถึง "Form 10", "Build-Form10Charts", "SPI Volume Control chart", "Xbar chart form", หรือถามเรื่องการสร้าง control chart จาก subgroup data ที่มีอยู่แล้วลงฟอร์มมาตรฐาน HANA (ไม่ใช่แค่โปรเจค SPI Volume Control เท่านั้น — pattern นี้ reuse ได้กับโปรเจคอื่นที่ต้อง fill Form 10 + native chart เหมือนกัน)
---

# Form 10 Rev A Control Chart Build

Workflow: มี subgroup data (Xbar/Range ต่อ subgroup) และ control limits (Xbar-bar/R-bar/UCL/LCL) คำนวณไว้แล้วในไฟล์ Excel อื่น → copy Form 10 Rev A template's `Data`+`CAR` sheet → เติม header/Group No./raw readings/live-formula stats → เพิ่ม native Excel Xbar chart + R chart (พร้อมเส้น CL/UCL/LCL) ต่อท้าย sheet โดยใช้ chart template ที่ save ไว้

**Reference implementation:** `D:\SPC\notes\Job\SPI volume test\Build-Form10Charts.ps1` (โปรเจค SPI Volume Control) — build ครบ 16 chart (3 method × 2 product × 2 metric, Method 3 แยก LED1/U1) สำเร็จ 2026-08-10 ดู [[project_spi_volume_control]] สำหรับ status ล่าสุด และ [[project_spc_knowledge_base]]'s Environment notes สำหรับ Excel-COM gotcha พื้นฐาน (batch write, name-diff sheet copy ฯลฯ) ที่ skill นี้ใช้ซ้ำ

## ไฟล์ที่เกี่ยวข้อง (SPI Volume Control instance)

- `D:\SPC\notes\Job\SPI volume test\001_018_000026_Form_10_Rev_A_xlsx.xlsx` — **template ตัวเปล่า** (`Data`+`CAR` sheet pair, ห้ามแก้ตรงๆ, เปิด read-only เสมอ) — formula สรุปผลเดิมในตัว (`Min/Max/Range/Average/Std.dev/Cpk` แถว 25-30) เสียหมด (`#REF!`/`#DIV/0!`) เขียนทับด้วย formula ใหม่ทุกครั้ง ไม่พึ่งของเดิม
- `D:\SPC\notes\Job\SPI volume test\Build-Form10Charts.ps1` — script หลัก, data-driven loop (methodDefs × productDefs × metricDefs) → 3 output workbook แยกตาม method
- `C:\Users\thadan\AppData\Roaming\Microsoft\Templates\Charts\controlchart.crtx` — saved Excel chart template (สไตล์/format) ที่ apply ทับ series ที่สร้างใหม่ผ่าน `Chart.ApplyChartTemplate(path)`
- Source data: `SPI Volume Control - Phase1 Subgroups.xlsx`'s `Method Comparison` sheet (control limits ต่อ combination) + `M{n}_Wide_*`/`M3_{component}_Wide_*` sheets (per-subgroup raw data) — **layout ต่างกันตาม method** (ดู Architecture)

## Architecture (ฟังก์ชันใน Build-Form10Charts.ps1)

- **`Get-MCRow`** — อ่าน control limits (N/XbarBar/RBar/UCLX/LCLX/UCLR/LCLR) จาก `Method Comparison` sheet โดย match Product/Method/Metric/Setup แบบ exact text
- **`Get-WideBoards`** (Method 1 layout) — 1 column-group ต่อ board, row1=board label, rows3-7=5 pad readings, row8=Xbar, row9=R
- **`Get-WideBoardsM2M3`** (Method 2/3 layout — **คนละ layout กับ Method 1 เลย**) — 2 row ต่อ block (header+data), data row cols 3/5/7/9/11=5 board values (Volume), 4/6/8/10/12=5 board values (Height), cols 13-16=Xbar/R Vol/Xbar/R Hgt — **ต้อง inspect sheet จริงก่อนเขียน reader ใหม่เสมอ ห้ามสันนิษฐาน layout จาก method อื่น** (บทเรียนจริง: ตอน generalize จาก M1-only pilot ไป M2/M3 เจอว่า layout ไม่เหมือนกันเลย)
- **`New-Form10Sheet`** — ฟังก์ชันหลัก generic เต็มที่ (ไม่ผูกกับ method/product ใดๆ) รับ `boards` (array ของ per-subgroup Label/Units/Xbar/R) + `mc` (control limits object) แล้ว: copy Data+CAR sheet, เติม header, เติม Group No./raw Unit readings, เขียน **live formula** MIN/MAX/RANGE/AVERAGE (ไม่ใช่ static value — Thada ขอเพราะอยากให้ตรวจสอบย้อนกลับได้), สร้าง hidden `_ChartData` helper sheet (คอลัมน์ Average/Range เป็น cross-sheet formula อ้างกลับไปที่ Data sheet's live formula เอง ไม่ใช่ค่าซ้ำอิสระ), สร้าง Xbar chart + R chart
- **`Copy-NamedSheet`** — identify sheet ที่เพิ่ง copy ด้วย name-diff (ดู gotcha ด้านล่าง)
- **`Reset-AxisScale`** / **`Set-AxisTitles`** / **`Set-PlotAreaMargins`** — เรียงตามลำดับหลัง `ApplyChartTemplate()` เสมอ (ดู gotcha)

## วิธี reuse กับโปรเจคใหม่

1. ยืนยันกับ Thada ก่อนว่าใช้ template `Form_10_Rev_A` ตัวเดิม หรือ template อื่น (ถ้าอื่น ต้อง map cell address ใหม่ — เช็คด้วย `Range.Find` ว่า field ไหนอยู่ตรงไหน อย่าสมมติ)
2. เขียน reader function ใหม่ที่อ่าน source data ของโปรเจคนั้น → คืนค่าเป็น array ของ `[PSCustomObject]@{ Label; Units (array 5 ค่า); Xbar; R }` ต่อ subgroup — **inspect sheet จริงก่อนเขียนเสมอ** (ตาม [[feedback_verify_with_example_before_full_run]])
3. เขียน control-limits lookup function ที่คืนค่า `[PSCustomObject]@{ N; XbarBar; RBar; UCLX; LCLX; UCLR; LCLR }`
4. เรียก `New-Form10Sheet` ตรงๆ (ฟังก์ชันนี้ generic แล้ว ไม่ต้องแก้)
5. **Build ตัวอย่างเดียวก่อนเสมอ (pilot-first)** แล้ว verify เลขตรงกับ source โดยเทียบมือ ก่อนขยายเป็น full loop — Thada ยืนยัน pattern นี้ใช้ได้ผลจริงตอนทำ SPI Volume Control (pilot 1 combo → verify → generalize 16 combo)

## Known gotchas (Excel COM automation, เจอจริงตอนทำ SPI Volume Control 2026-08-10)

- **เขียนทีละ cell พังแบบสุ่ม** (`InvalidCastException`, template cell มี custom style เสีย `Normal_509#12`) — แก้ด้วย **batch `Range.Value = array` write เสมอ** (1D array แถวเดียว, `New-Object 'object[,]' (rows,cols)` สำหรับ block สี่เหลี่ยม, ใช้ genuine 2D `(n,1)` array สำหรับ column แนวตั้ง — flat 1D ใช้กับ column ไม่ได้) — ใช้ได้กับทั้ง `.Value` และ `.Formula`
- **`Worksheet.Copy(After:=X)` เพี้ยนตำแหน่งเมื่อ X เป็น hidden sheet** — Excel แทรกก่อนหน้าแทนที่จะแทรกหลัง ทำให้ "sheet ตัวสุดท้ายตาม index" ผิด — แก้ด้วย name-diff (เทียบชื่อ sheet ก่อน/หลัง copy)
- **ชื่อ sheet เกิน 31 ตัวอักษรเมื่อรวม suffix** — เผื่อพื้นที่ suffix ที่ยาวที่สุด (`_ChartData` = 10 ตัวอักษร) ไว้ล่วงหน้าเสมอ
- **`ApplyChartTemplate()` สืบทอด axis scale (Max/MajorUnit) และ axis-title position แบบ absolute จาก template เดิม** — ต้อง reset ทุกครั้งหลัง apply: `MinimumScaleIsAuto`/`MaximumScaleIsAuto`/`MajorUnitIsAuto`=`$true`, และ toggle `HasTitle=$false` แล้ว `$true` ใหม่ก่อนตั้ง `.AxisTitle.Text` (ไม่ใช่แค่ตั้ง `.Text` เฉยๆ — position เก่าจะทับ text ใหม่)
- **PlotArea ไม่ auto-resize ให้ axis title ที่เพิ่มทีหลัง** — ต้อง pin `PlotArea.Width/Height/Left/Top` เอง (fixed margin) และ**เรียก `ChartObject.Activate()` ก่อน set PlotArea properties เสมอ** (ไม่งั้น throw `COMException E_FAIL`) — set `Width`/`Height` ก่อน `Left`/`Top` (ลำดับมีผล)
- **`Chart.Export()` เป็น PNG ต้อง Excel visible + activate chart ก่อน** — ถ้า `$excel.Visible=$false` จะได้ไฟล์ 0 byte แบบเงียบๆ (return `$true` ด้วยซ้ำ) ต้อง `$excel.Visible=$true` + `$chartObject.Activate()` + `Start-Sleep -Milliseconds 300` ก่อน export
- **Transient COM/resource error ระหว่างรัน script ซ้ำๆติดกันหลายรอบ** (`OutOfMemoryException`, `CO_E_SERVER_EXEC_FAILURE`, paging-file-too-small) — เช็ค `Get-Process EXCEL` ก่อนเสมอ ถ้าไม่มี process ค้างจริง มักเป็นแค่ resource ตึงชั่วขณะ retry เฉยๆ ก็ผ่าน ไม่ต้องไล่ debug โค้ด
