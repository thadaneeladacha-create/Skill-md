# OEE Downtime Tracker — Skill Note

## Context

สร้างเว็บแอปบันทึก Downtime เพื่อนำข้อมูลไปคำนวณ OEE (Overall Equipment Effectiveness)
โปรเจคอยู่ที่ `D:\project\OEE-Downtime-Tracker`

---

## Tech Stack

| Layer    | Technology                                           |
| -------- | ---------------------------------------------------- |
| Frontend | HTML / CSS / Vanilla JS + Flatpickr 4.6.13 (date/time picker) |
| Backend  | Python 3.13 + Flask 3.x (port 3000)                 |
| Storage  | SQLite (`data/oee.db`) — migrate จาก JSON อัตโนมัติ  |
| Export   | CSV download (UTF-8 BOM สำหรับ Excel)                |
| Runtime  | Embeddable Python (offline, ไม่ต้องติดตั้ง)          |
| Fallback | `OEE_Downtime_Form.xlsx` กรณีระบบล่ม                |

---

## Project Structure

```
OEE-Downtime-Tracker/
├── app.py                    ← Flask API server
├── start.bat                 ← Double-click เปิดแอป (auto-detect Python)
├── setup_offline.bat         ← รันบน dev machine ครั้งเดียว (ต้องอินเตอร์เน็ต)
├── create_excel_form.py      ← script สร้าง Excel backup form
├── OEE_Downtime_Form.xlsx    ← แบบฟอร์ม Excel สำรอง
├── seed_test.py              ← dev only — ใส่ข้อมูลทดสอบ
├── python-embed-313-64/      ← Python 3.13.3 (Windows 10/11 64-bit)
├── python-embed-38-64/       ← Python 3.8.10 (Windows 7 64-bit)
├── python-embed-38-32/       ← Python 3.8.10 (Windows 32-bit ทุกรุ่น)
├── public/
│   ├── index.html
│   ├── style.css
│   ├── app.js
│   ├── flatpickr.min.js      ← date/time picker (bundled offline)
│   └── flatpickr.min.css
└── data/
    └── oee.db                ← SQLite (สร้างอัตโนมัติตอน startup)
```

---

## วิธีรัน

### บนเครื่อง Dev (มี Anaconda)

```
ดับเบิลคลิก start.bat
```

### บนเครื่องปลายทาง (ไม่มี Python / ไม่มีอินเตอร์เน็ต)

**ทำบนเครื่อง dev ครั้งเดียว (ต้องมีอินเตอร์เน็ต):**

1. ดับเบิลคลิก `setup_offline.bat`
2. จะ download + install Python 3 ตัวและ Flask ทั้งหมดอัตโนมัติ

**Copy ทั้ง folder** ไปเครื่องปลายทาง

**บนเครื่องปลายทาง:** ดับเบิลคลิก `start.bat` ได้เลย

---

## Offline Deployment — Multi-OS

`setup_offline.bat` download Python เวอร์ชันที่เหมาะสม 3 ตัว:

| Folder | Python Version | สำหรับ |
|--------|---------------|--------|
| `python-embed-313-64` | 3.13.3 amd64 | Windows 10/11 64-bit |
| `python-embed-38-64`  | 3.8.10 amd64 | Windows 7 64-bit |
| `python-embed-38-32`  | 3.8.10 win32 | Windows 32-bit ทุกรุ่น |

> Python 3.8.10 คือ version สุดท้ายที่มี embeddable package และรองรับ Windows 7
> Python 3.8.20 (ตัวเลขสูงกว่า) ไม่มี embeddable package บน python.org

`start.bat` ตรวจสอบ OS + architecture อัตโนมัติ:
- `%PROCESSOR_ARCHITECTURE%` → AMD64=64bit / x86=32bit
- `ver` command → token 4 → 6=Win7, 10=Win10/11
- Fallback chain: prefer → 313-64 → 38-64 → 38-32 → python-embed → system python

---

## Browser Compatibility

เว็บใช้ **Flatpickr 4.6.13** (bundled, ไม่ต้องอินเตอร์เน็ต) แทน `type="date"` และ `type="time"` เพราะ Internet Explorer และ Edge Legacy ไม่รองรับ native input เหล่านี้

- `input[type="date"]` → `input[type="text"]` + Flatpickr calendar
- `input[type="time"]` → `input[type="text"]` + Flatpickr time picker (24h)
- Lot time inputs: init Flatpickr ผ่าน `initLotRow()` ทุกครั้งที่สร้าง row

**Pitfall**: `Set-Content -Encoding UTF8` ใน PowerShell 5.1 เพิ่ม BOM ทำให้ Python อ่าน `.pth` ไม่ได้ → ใช้ `[System.Text.UTF8Encoding]::new($false)` แทน

---

## Features

### เครื่องจักร
AD05 – AD38 (dropdown)

### Group & Shift — Sticky Fields
Group (A/B/C) และ Shift (Day/Night) ไม่ reset หลังบันทึก

### 5 Action Types

| Action          | Extra Field                                    |
| --------------- | ---------------------------------------------- |
| Working         | Lot + เวลาเริ่ม/จบ ต่อ Lot (เพิ่มได้หลาย Lot) |
| Daily Check     | —                                              |
| Machine Trouble | —                                              |
| รองาน           | —                                              |
| อื่นๆ           | ช่องระบุเหตุผล (textarea)                      |

### Midnight Crossing Detection
- endTime < startTime → บวก 1,440 นาทีอัตโนมัติ
- แสดง badge "+1วัน" ในฟอร์มและตาราง

### Machine Availability

```
Availability = (Plan Time − Downtime) / Plan Time × 100
```

- Day Shift: 720 นาที (05:00–17:00)
- Night Shift: 720 นาที (17:00–05:00)
- Downtime = ผลรวมนาทีที่ไม่ใช่ Working
- Badge: เขียว ≥85%, เหลือง 70–84%, แดง <70%

### Edit / Delete / Pagination / Filter
- Sort: `date DESC, startTime DESC` (ไม่ใช่ savedAt — ป้องกัน record กระโดดหลัง edit)
- Pagination: 50 records/หน้า
- Filter: เครื่อง / Group / Shift / Action (client-side)

---

## Excel Backup Form (`OEE_Downtime_Form.xlsx`)

สร้างด้วย `create_excel_form.py` (openpyxl)

| Column | Field | Feature |
|--------|-------|---------|
| A | วันที่ | format YYYY-MM-DD |
| B | เครื่องจักร | dropdown AD05–AD38 |
| C | Group | dropdown A/B/C |
| D | Shift | dropdown Day/Night |
| E | Action | dropdown + color coding |
| F | Lot / เหตุผล | free text |
| G | เวลาเริ่ม | format HH:MM |
| H | เวลาจบ | format HH:MM |
| I | ระยะเวลา (นาที) | `=ROUND(MOD(H-G,1)*1440,0)` auto-calc + midnight |
| J | หมายเหตุ | free text |

- 300 แถว, freeze header, auto-filter
- Conditional formatting สีตาม Action (ตรงกับเว็บ)
- Sheet `_Lists` (hidden) เก็บ dropdown values
- Sheet `คำแนะนำ` อธิบายวิธีใช้

---

## API Endpoints

```
GET    /api/records        → ดึงข้อมูลทั้งหมด
POST   /api/records        → บันทึกรายการใหม่
DELETE /api/records/:id    → ลบรายการ
GET    /api/export         → Download CSV
```

---

## SQLite Schema

```sql
CREATE TABLE records (
    id        TEXT PRIMARY KEY,
    savedAt   TEXT,
    date      TEXT,
    machine   TEXT,
    grp       TEXT,   -- ใช้ grp เพราะ group เป็น reserved word
    shift     TEXT,
    action    TEXT,
    lots      TEXT,   -- JSON string
    reason    TEXT,
    startTime TEXT,
    endTime   TEXT,
    duration  REAL
);
```

Migration จาก `records.json` → SQLite รันอัตโนมัติครั้งเดียวตอน startup

---

## Conversation Reference

สร้าง: 2026-05-14 | อัปเดตล่าสุด: 2026-05-15

การเปลี่ยนแปลงหลักตลอดการพัฒนา:
- Storage: JSON → SQLite
- Deployment: Anaconda → Embeddable Python (Multi-OS)
- Browser: native date/time input → Flatpickr (IE/Edge compatible)
- เพิ่ม Machine Availability panel
- Day shift plan time: 720 นาที (05:00–17:00)
- เพิ่ม Edit / Delete / Pagination / Midnight detection
- เพิ่ม Excel backup form
