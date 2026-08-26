---
name: mitutoyo-flask-vba
description: ใช้ skill นี้เมื่อ Thada ทำงานต่อ Mitutoyo project — ฟอร์ม Excel + VBA macro ที่รับค่าจากเครื่องจักร/เครื่องมือวัดผ่าน REST API ที่รันบน Flask — trigger เมื่อพูดถึง "Mitutoyo project", "flask server สำหรับ VBA", "mod_FlaskAPI", "ต่อยอด flask กับ excel", "เครื่องจักรยิง API", หรือถามเรื่องไฟล์ใน D:\SPC\notes\Job\Mitutoyo project
---

# Mitutoyo Project — Flask ↔ Excel VBA

Concept: เครื่องจักร/เครื่องมือวัด (Mitutoyo) ยิงค่าออกมาเป็น REST API บน Flask → Excel ใช้ VBA (WinHttp, ไม่ต้อง reference เพิ่ม) ดึงค่าเข้าฟอร์ม SPC โดยอัตโนมัติ

ตอนนี้อยู่ในขั้น **ทำ Flask จำลอง (simulator) ไว้ทดสอบ VBA macro บนเครื่องตัวเอง** ก่อน — ยังไม่ได้ต่อกับเครื่องจักร Mitutoyo จริง รอหัวหน้ามอบหมาย scope ต่อไป (มอบหมายล่าสุดตรวจสอบ ณ 2026-07-21)

## ไฟล์ที่เกี่ยวข้อง

- `D:\SPC\notes\Job\Mitutoyo project\mod_FlaskAPI.bas` — VBA module ที่ import เข้า Excel
- `D:\SPC\notes\Job\Mitutoyo project\flask_server\app.py` — Flask simulator (จำลองเครื่องจักรส่งค่า)
- `D:\SPC\notes\Job\Mitutoyo project\flask_server\requirements.txt` — มีแค่ `flask`
- `D:\SPC\notes\Job\Mitutoyo project\flask_server\run_server.bat` — ดับเบิลคลิกรัน server (cd เข้าโฟลเดอร์ตัวเองอัตโนมัติ + pause)

## Endpoint ↔ VBA sub mapping

| Flask endpoint | Method | เรียกจาก VBA | ใช้ทำอะไร |
|---|---|---|---|
| `/api/data` | GET | `GetMachineData` → `RefreshFormFromMachine` | ค่า flat JSON (temperature, pressure, status) ใส่ฟอร์ม B2:B5 — **นี่คือ sub หลักถ้าต้องการแค่รับค่าเข้าฟอร์มอย่างเดียว** |
| `/api/machine/status` | GET | `GetMachineData` | สถานะเครื่อง + timestamp |
| `/api/measurement` | GET | ยังไม่มี VBA เรียก (เตรียมไว้) | ค่าที่วัดได้จริงสไตล์เครื่องมือวัด: measured_value, nominal/USL/LSL, judge OK/NG — ใช้ต่อยอดตอนทำฟอร์ม SPC รับค่าวัดชิ้นงานจริง |
| `/api/setpoint` | POST | `PostMachineData` → `SendFormToMachine` | ตัวอย่างส่งค่ากลับไปเครื่องจักร (echo กลับ) — ใช้เฉพาะกรณีเครื่องจักรควบคุมได้สองทาง (two-way) ถ้าเครื่องมือวัดจริงเป็นแบบรับอย่างเดียว (one-way) sub นี้ไม่จำเป็น |

## วิธีรันทดสอบ

```
cd "D:\SPC\notes\Job\Mitutoyo project\flask_server"
python -m pip install -r requirements.txt   # ครั้งแรกครั้งเดียว
python app.py                                # หรือดับเบิลคลิก run_server.bat
```

ใน `mod_FlaskAPI.bas` ตั้ง `API_BASE_URL = "http://127.0.0.1:5000"` (เครื่องเดียวกัน) หรือ IP ของเครื่องที่รัน Flask (server ฟังที่ `0.0.0.0:5000` รองรับ LAN อยู่แล้ว)

## Known gotchas

- **VBA `.bas` ต้อง encoding เป็น Windows-874 (Thai ANSI) + CRLF ไม่ใช่ UTF-8** — ถ้าเขียน/แก้ไฟล์ `.bas` แล้วมี comment ภาษาไทย ต้อง save/convert เป็น cp874 ไม่งั้น VBA editor (ตัวเก่า ไม่รองรับ Unicode) จะอ่านเพี้ยน วิธี convert ด้วย python:
  ```python
  text = open(path, encoding="utf-8").read().replace("\n", "\r\n")
  open(path, "wb").write(text.encode("cp874"))
  ```
- **ถ้า convert เป็น cp874 แล้วยังอ่านเพี้ยนใน VBA editor** — เป็นปัญหา font ของ editor ไม่ใช่ encoding (เช็คได้โดย copy ข้อความออกมาวางที่อื่น ถ้าอ่านออกแปลว่า encoding ถูกแล้ว) แก้ที่ Tools → Options → Editor Format → Font → เปลี่ยนเป็นฟอนต์ที่รองรับไทย เช่น Tahoma, Leelawadee UI
- `ExtractJsonValue` ใน `mod_FlaskAPI.bas` เป็น parser มือ รองรับเฉพาะ JSON แบบ flat (ไม่ nested) ถ้า endpoint ไหนมี JSON ซับซ้อนกว่านี้ต้อง import [VBA-JSON](https://github.com/VBA-tools/VBA-JSON) แทน
