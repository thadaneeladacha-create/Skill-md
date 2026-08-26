---
name: nested-grr-excel
description: "Compute nested Gage R&R (destructive test) directly in Excel — replaces the Minitab step. Builds ANOVA + variance components with traceable formulas, links the IV. Result section, and recreates the 5 Minitab-style charts."
metadata:
  type: claude-skill
  stack: Excel, Office.js, VBA
---

# Nested Gage R&R in Excel — Skill Note

## Context

Claude Code skill (`nested-grr-excel`) ที่ทำ Nested Gage R&R (destructive test) ทั้งหมดด้วยสูตร Excel แทนการพึ่ง Minitab
Output ป้อนเข้าแบบฟอร์ม GRR แบบ "WPT" (wire-pull-test style): calc sheet + link เข้า IV. Result cells + สร้างกราฟ 5 แบบสไตล์ Minitab

**ใช้เมื่อ:** มีแบบฟอร์ม destructive-test GRR (เช่น wire-pull "WPT" sheet) และอยากได้ nested Gage R&R ใน Excel แทนการ copy ผลจาก Minitab
Design ต้อง nested (parts nested within operators, replicates within parts) — destructive test เป็น nested เสมอเพราะวัดซ้ำชิ้นเดิมไม่ได้
**ไม่ใช้กับ** crossed studies (operator ทุกคนวัด part เดียวกันแบบ non-destructive) — สูตร reproducibility ต่างกัน

---

## Step 1 — อ่าน raw data layout

อ่านส่วน "II. Data" ของฟอร์ม ระบุ: operator IDs, จำนวน operators `a`, parts ต่อ operator `p`, reps ต่อ part `n`, และ cell range ของแต่ละ operator (กลุ่มตาม part, n reps ต่อ part) ยืนยัน total N = a·p·n

## Step 2 — สร้างชีต "GRR Calc" (สูตร traceable, link ไป raw data)

สร้าง/แทนที่ชีต `GRR Calc` อ้างอิง cell ดิบด้วยสูตร (เช่น `='WPT '!E23`) — **ห้าม paste ตัวเลขนิ่ง** (ระวังชื่อชีตอาจมี trailing space)

**Part-level table** (1 แถวต่อ part = a·p แถว): Operator, Part, Rep1..Repn, `Mean =AVERAGE(reps)`, `Range =MAX(reps)-MIN(reps)`, `SS within =DEVSQ(reps)`

**Design & means:** cell label `a`, `p`, `n`; `Grand =AVERAGE(all)`; mean ต่อ operator

**Nested ANOVA table** (Source/DF/SS/MS):
- Operator: DF `=a-1`; SS `=p*n*SUMPRODUCT((opMeans-grand)^2)`; MS=SS/DF
- Part(Operator): DF `=a*(p-1)`; SS `=n*Σ(partMeans_op-opmean)^2` ต่อ operator; MS=SS/DF
- Repeatability: DF `=a*p*(n-1)`; SS `=SUM(SS within column)`; MS=SS/DF
- Total: DF `=a*p*n-1`; SS `=DEVSQ(all readings)`

**Validation:** SS_Operator + SS_Part + SS_Repeat ต้องเท่ากับ SS_Total เป๊ะ ถ้าไม่เท่า แสดงว่า range ผิด

**Variance components** (nested — จุดต่างหลักจาก crossed):
- Repeatability (EV): `=MS_rep`
- Reproducibility (AV): `=MAX((MS_op - MS_part)/(p*n), 0)` ← test operator กับ Part(Operator), ไม่ใช่ error, floor ที่ 0
- Part-to-Part (PV): `=MAX((MS_part - MS_rep)/n, 0)`
- Total Gage R&R: `=EV + AV`
- Total Variation (TV): `=GRR + PV`

แต่ละตัว: `%Contribution =VarComp/TV`; `SD =SQRT(VarComp)`; `StudyVar =6*SD`; `%StudyVar =SD/SD_total`
`ndc =1.41*SD_PV/SD_GRR`

## Step 3 — Link IV. Result section ของฟอร์ม

ฟอร์มอ้าง `(EV/TV)*100` = %Study Var (SD-basis) ไม่ใช่ %Contribution — ต้อง link ให้ถูกคอลัมน์:
- %Repeatability ← %StudyVar ของ EV; %Reproducibility ← AV; %GRR ← Gage R&R; %PV ← Part-to-Part; ndc ← `=ROUND(ndc,0)`
Disposition (<=10% / 10–30% / >30%) มักคีย์จาก %GRR อัตโนมัติ
**Sanity check:** `SQRT(%GRR^2 + %PV^2)` ≈ 100% — ถ้าฟอร์มมี %PV hardcode ที่ fail check นี้ แปลว่าเป็น typo จากการ copy Minitab

## Step 4 — สร้างกราฟ 5 แบบสไตล์ Minitab (nested ไม่มี interaction panel)

Build chart-source blocks บน GRR Calc แล้วเพิ่มกราฟที่ฟอร์มชีตในส่วน "III. Graph Attach" ผ่าน `execute_office_js`

**Enum casing gotcha:** ChartType ต้องเป็นตัวพิมพ์เล็ก: `xyscatter`, `xyscatterLines`, `boxwhisker` (ไม่ใช่ `xyScatter`/`boxWhisker` → InvalidArgument) การตั้ง `chart.title.text` ไม่เปลี่ยน `chart.name` (ยังเป็น "Chart 41") — ถ้าจะ delete-by-name ทีหลังจะพลาด ต้องตั้ง `chart.name` เอง หรือ delete โดย match `title.text`

SPC constants (n=3): d2=1.69257, D4=2.574, A2=1.023 (ค่า n อื่นดูตาราง lookup)

1. **Components of Variation** — clustered column: Gage R&R/Repeat/Reprod/Part-to-Part × %Contribution & %Study Var
2. **R Chart by Operator** — line: Range ต่อ part, CL=Rbar, UCL=D4·Rbar, LCL=0 label ค่า limit แบบ Minitab: data label เฉพาะจุดสุดท้ายของ CL/UCL/LCL (`showValue`, `showSeriesName`, `separator="="`, `position=right` → "UCL=1.625")
3. **MS value by Part** — XY scatter ของ raw reading ทั้งหมด (X=part index ซ้ำ n ครั้งต่อ part, Y=แต่ละ reading) + series mean-connect แยก (`xyscatterLines`) — ห้าม plot แค่ mean เพราะ Minitab โชว์ทุกจุด
4. **Xbar Chart by Operator** — line: part means, CL=grand, UCL/LCL=grand±A2·Rbar + label แบบเดียวกับ R chart
5. **MS value by Operator** — box & whisker: 1 คอลัมน์ raw values ต่อ operator (seriesBy columns) เปิด legend ให้โชว์ label operator (ไม่งั้น category axis จะขึ้นแค่ "1")

หลัง `charts.add` collection ที่ load ไว้ก่อนหน้าจะ stale ต้อง reload ใหม่

### Optional — เส้นแบ่ง operator + label (สไตล์ Minitab) บน R & Xbar chart

Divider แนวตั้ง (self-aligning): helper series 2 จุด X=(p,p) via `=p`, Y=(0, primaryValueAxisMax) บน secondary axis — ต้อง set values/xAxisValues/chartType/axisGroup ทั้งหมดก่อน sync ครั้งแรก (reuse series ข้าม sync จะ throw trackedObjects error) ตั้ง secondary category axis min=0/max=a·p/visible=false และ secondary value axis min=0/max=primary max/visible=false — format เส้น dash สีเทา `line.weight` ต้องเป็น integer

Label operator เหนือแต่ละช่วง: scatter series 2 จุด (markerStyle none) ที่ X=group center (p/2, 1.5·p) label แบบ dynamic ผ่าน `point.dataLabel.formula = "='GRR Calc'!$A$4"` (ไม่ใช่ static text) — cross-sheet ref ใช้ `!` ไม่ใช่ `.` ซ่อน helper series จาก legend ผ่าน `legendEntries.getItemAt(i).visible=false`

Caveat: เฉพาะ label TEXT dynamic — ตำแหน่ง divider/label สมมติ fixed 2-operator design ต้อง extend เองถ้ามี 3+ operators

## Step 5 — Verify

อ่าน calc sheet + linked result cells ใหม่ ยืนยัน: SS additivity, ไม่มี #REF!/#VALUE!, %GRR band ขับ disposition ถูก, sqrt(%GRR²+%PV²)≈100%, ndc round สมเหตุสมผล render graph region เช็ค layout

---

## Reference values (wire-pull example, a=2,p=5,n=3)

%EV=25.63%, %AV=0%, %GRR=25.63%, %PV=96.66%, ndc≈5.3→5ตรงกับ Minitab เป๊ะ — ใช้เป็น smoke test ของ method ไม่ใช่ผลลัพธ์ที่คาดหวังสำหรับข้อมูลใหม่

---

## Optional — ทำ calc dynamic รองรับ operator count ใดก็ได้ (balanced design)

- เก็บ operator ID 1 ค่าต่อแถว part (ห้าม merge cell operator — merge จะ blank แถวล่างและพัง formula ต่อแถว) pre-size ตาราง part ให้ generous (เช่น 30 แถว), guard แถวว่าง: `Mean =IF(COUNT(reps)=0,"",AVERAGE(reps))`, `SS within =IF(COUNT(reps)=0,0,DEVSQ(reps))`
- Helper columns ต่อแถว (วางไกลขวาสุด พ้น chart-data block): `OpMean =IF(A="","",AVERAGEIF(opCol,A,meanCol))`; `devOp =IF(A="",0,(OpMean-grand)^2)`; `devPart =IF(A="",0,(Mean-OpMean)^2)`
- SS แบบ dynamic ทั้ง block: `SS_op =n*SUM(devOp)`, `SS_part =n*SUM(devPart)`, `SS_rep =SUM(SSwithin)`
- Auto-detect design: `a =SUMPRODUCT((opCol<>"")/COUNTIF(opCol,opCol&""))`; `p =COUNTIF(opCol,firstOpCell)`; `n` เป็น input — DF/MS/variance/%StudyVar/ndc ตามมาอัตโนมัติ
- เพิ่ม capacity ตารางโดยไม่พัง chart-data block ทางขวา: ใช้ `range.insert(Excel.InsertShiftDirection.down)` เฉพาะคอลัมน์ตาราง (เช่น A14:H33) ห้าม insert ทั้งแถว (จะ clip chart-source block ที่คร่อมแถวนั้น) การ insert cell/row จะอัพเดต cross-sheet link (IV.Result, chart data) ให้อัตโนมัติ
- Caveat: เฉพาะ**ตัวเลข**ที่ dynamic กราฟ 5 แบบยังอ้าง range operator/point เดิม ต้อง extend series/box column เองเวลาจำนวน operator เปลี่ยนจริง

---

## Optional — VBA macro "RebuildGRRCharts" (dynamic operator count, ไฟล์ที่ใช้โดยไม่มี add-in)

Divider/labels/data-ranges ใน Step 4 ไม่ auto-dynamic (axis min/max ไม่ใช่ formula-driven, label text ต่อจุดต้องใช้โค้ด) ถ้าแชร์ workbook กับคนที่ไม่มี add-in นี้และ operator count เปลี่ยน ให้ VBA macro ไปรันเอง (save เป็น .xlsm, Enable Macros) — Office Scripts ใช้ไม่ได้บน perpetual Excel (2019/2021, ไม่มี Automate tab) จึงต้องใช้ VBA

**Architecture:** อ่าน a=B36, p=B37; N=a*p แต่ละ control chart (หาโดย `ChartTitle.Text`): (1) rewrite data block ใหม่ในพื้นที่ว่างไกลขวา — คอลัมน์ Sample/val/CL/UCL/LCL แถว 2..1+N เป็นสูตรลิงก์ตาราง part (`=B{4+i}`, CL/UCL/LCL จาก SPC constant cells) (2) `RepointSeries` series เดิมไป range ใหม่ (3) สร้าง a-1 dividers เป็น 1 series `xlXYScatterLinesNoMarkers` จุดคู่ (x=k*p,y=0),(x=k*p,y=axisMax) คั่นด้วยแถวว่าง (blank = ตัดเป็น segment) (4) สร้าง a labels เป็น 1 series `xlXYScatter` (MarkerStyle none) ที่ x=(k+0.5)*p, y=axisMax*0.95 — ทั้ง 2 helper series ใช้ `AxisGroup=xlSecondary`

**Hard-won VBA gotchas:**
- VBA case-INSENSITIVE: ห้าม declare ทั้ง `n` และ `N` ใน scope เดียวกัน ("ambiguous name") — ใช้แค่ N=total points
- `Chart.Axes(...)` คืน `Object` ไม่ใช่ `Axis` — helper `Sub HideAxis(ByVal ax As Object, ByVal mn As Double, ByVal mx As Double)` กัน "ByRef argument type mismatch"
- ก่อน scale secondary axes ต้อง force ให้มีอยู่ก่อน: `cht.HasAxis(xlValue, xlSecondary) = True` และ `cht.HasAxis(xlCategory, xlSecondary) = True` ไม่งั้น throw + divider/label เพี้ยน ตั้ง secondary category(X) min=0/max=a*p, secondary value(Y) min=0/max=axisMax แล้วซ่อนทั้งคู่
- Data labels: ต้องตั้ง POINT-level `.Points(k+1).HasDataLabel = True` ก่อน (series-level `HasDataLabels=True` เฉยๆ จะได้ `.DataLabel` = Nothing → err 91) แล้วค่อย `.DataLabel.Text = <operator ID>` ตรงๆ ห้ามตั้ง `.ShowSeriesName/.ShowValue/.ShowCategoryName` (throw "Parameter not valid" + label โชว์ raw Y value แทน) label แบบนี้ static (refresh-on-run) ไม่ live-link แบบ Office.js `ChartDataLabel.formula`
- Stability: `Application.Calculation = xlCalculationManual` + `EnableEvents = False` ตลอดรัน (แก้ chart series ระหว่าง auto-recalc ทำ Excel crash) restore ผ่าน `Cleanup:` label ที่ reach ด้วย `Resume Cleanup` จาก error handler ลบ helper series เก่าแบบ scan-one-delete-restart loop (backward-index delete loop ทำ crash ได้)
- Debug ทางไกล: เก็บ module-level `gStep` string อัพเดตก่อนทุก step เสี่ยง แล้วโชว์ใน handler (`"Error at [" & gStep & "]: " & Err.Description`)

Caveat: เฉพาะตัวเลข + 2 control chart นี้ที่ adapt อัตโนมัติ กราฟอื่นยัง extend range เอง

### VBA rebuild — bake สี series

สีที่ตั้งมือจะ reset เป็น auto ทุกครั้งที่ rebuild ต้อง bake เข้า macro ตัวอย่างที่ใช้บ่อย: main data line สีกรมท่าเข้ม `RGB(0, 32, 96)` (#002060) ที่เหลือปล่อย auto palette (ตรงกับ Minitab style อยู่แล้วสำหรับ CL/UCL/LCL, Components bars, box fills) หลังสร้างแต่ละ chart loop `cht.SeriesCollection`: main value series (name = valName / "Mean") ตั้ง `.Format.Line.ForeColor.RGB`, `.MarkerForegroundColor`, `.MarkerBackgroundColor` เป็นสีกรมท่า; by-part "Rep" marker series ตั้ง `.MarkerForegroundColor` กรมท่า (border) + `.MarkerBackgroundColorIndex = xlColorIndexNone` (hollow marker กัน reps ที่ overlap อ่านไม่ออก) ห้าม recolor CL/UCL/LCL ถ้าไม่ได้ขอ

---

## Conversation Reference

Sync จาก Claude Code skill `nested-grr-excel` (`C:\Users\thadan\.claude\skills\nested-grr-excel\SKILL.md`) — 2026-07-20
