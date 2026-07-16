# Claudian on Obsidian — Install Guide (Windows)

คู่มือติดตั้ง [Claudian](https://github.com/YishenTu/claudian) — ปลั๊กอิน Obsidian ที่ฝัง Claude Code CLI
เป็น chat sidebar โดยให้ vault เป็น working directory ของ agent

เขียนจากการติดตั้งจริงบนเครื่องส่วนตัว 2026-07-16 (Claudian 2.0.34)
**พกพาได้ — ไม่มี path เฉพาะเครื่อง ใช้คำสั่งค้นหาเอาแทน**

> วิธีใช้ไฟล์นี้กับเครื่องใหม่: เปิด Claude Code ที่เครื่องนั้นแล้วบอกว่า
> *"อ่าน install-guide.md นี้แล้วติดตั้ง Claudian ให้หน่อย"* — ไกด์นี้เขียนให้ agent อ่านรู้เรื่อง

---

## 1. Prerequisites — เช็คก่อน

```powershell
node --version      # ต้องมี (Claudian spawn CLI ผ่าน node)
npm --version
npm ls -g --depth=0 # ต้องเห็น @anthropic-ai/claude-code
```

- **Obsidian ≥ 1.7.2** (desktop เท่านั้น — ไม่รองรับ mobile)
- **Claude Code CLI** ติดตั้งแล้ว + login แล้ว (subscription หรือ API key)
  - เช็ค auth: มีไฟล์ `%USERPROFILE%\.claude\.credentials.json` = login แล้ว
  - Claudian ใช้ auth เดิม **ไม่ต้อง login ใหม่**

---

## 2. Gotchas — อ่านก่อน ไม่งั้นเสียเวลา

README ของ repo บอกไม่ตรงกับความจริง 2 จุด:

1. **ไม่มีใน Obsidian community store**
   README บอกให้ Browse แล้ว search "Claudian" — **หาไม่เจอ** เช็ค
   `obsidianmd/obsidian-releases/community-plugins.json` แล้วไม่มีชื่อ
   → ต้องติดตั้ง manual จาก GitHub release เท่านั้น (และไม่มี auto-update)

2. **Plugin id คือ `realclaudian` ไม่ใช่ `claudian`**
   README บอกให้สร้างโฟลเดอร์ชื่อ `claudian` แต่ `manifest.json` จริงคือ `"id": "realclaudian"`
   → **ตั้งชื่อโฟลเดอร์ `realclaudian`** ให้ตรง id (Obsidian keyed สถานะ enable ด้วย id)

อีก 2 จุดที่เจอตอนติดตั้งจริง:

3. **npm shim ของ `claude` อาจพัง** — ถ้า `claude` ใน PowerShell ขึ้น
   *"not recognized"* ทั้งที่ `npm ls -g` เห็นแพ็กเกจ ให้ดูใน `%APPDATA%\npm`
   ถ้าเจอไฟล์แปลก ๆ อย่าง `.claude-xxxxx`, `.claude.cmd-xxxxx` = shim ค้างจาก install ที่ถูกขัดจังหวะ
   **ไม่ต้องแก้ก็ได้** เพราะขั้นตอนที่ 5 ชี้ไป `cli-wrapper.cjs` ตรง ๆ อยู่แล้ว
   (จะซ่อมก็ `npm install -g @anthropic-ai/claude-code` ใหม่)

4. **CLI path เก็บแยกตามเครื่อง** — ใน settings เก็บใต้ `cliPathsByHost` keyed ด้วย device id
   → **ต่อให้ sync settings ข้ามเครื่อง path ก็ไม่ตามไป ต้องตั้งใหม่ทุกเครื่อง**

---

## 3. สร้างโฟลเดอร์ + โหลดไฟล์

เช็ค release ล่าสุดที่ https://github.com/YishenTu/claudian/releases (ตอนเขียน = `2.0.34`)

```powershell
$vault = "PATH\TO\YOUR\VAULT"          # <-- แก้ตรงนี้
$tag   = "2.0.34"                       # <-- เช็ค release ล่าสุดก่อน
$dir   = "$vault\.obsidian\plugins\realclaudian"

New-Item -ItemType Directory -Force -Path $dir | Out-Null
foreach ($f in @("main.js","manifest.json","styles.css")) {
  Invoke-WebRequest -Uri "https://github.com/YishenTu/claudian/releases/download/$tag/$f" `
                    -OutFile "$dir\$f" -UseBasicParsing
}
Get-ChildItem $dir | Select-Object Name, Length
```

**ตรวจว่าได้ของจริง**: `main.js` ควรราว 4 MB+, `styles.css` ราว 130 KB,
`manifest.json` ต้องมี `"id": "realclaudian"` — ถ้า `main.js` เล็กผิดปกติแปลว่าได้หน้า HTML error มา

---

## 4. เปิดใช้ใน Obsidian (ทำใน UI)

1. เปิด Obsidian ที่ vault นั้น
2. Settings → Community plugins → **Turn off Restricted Mode**
3. Reload แล้วเปิดสวิตช์ **Claudian**

> อย่าแก้ `.obsidian\community-plugins.json` เองตอนแอปเปิดอยู่ — Obsidian cache ไว้ในหน่วยความจำ จะถูกเขียนทับ

---

## 5. ตั้ง Claude CLI path (ขั้นตอนที่คนพลาดบ่อยสุด)

หา path ของเครื่อง **นั้น** (อย่าก๊อป path จากเครื่องอื่น):

```powershell
# npm install:
Write-Output ((npm root -g) + "\@anthropic-ai\claude-code\cli-wrapper.cjs")

# native install:
where.exe claude
```

ทดสอบก่อนว่ารันได้จริง:
```powershell
node "<path ที่ได้>" --version     # ต้องตอบเวอร์ชันกลับมา
```

แล้วใส่ที่ **Settings → Claudian → Advanced → Claude CLI path**

> **ช่องนี้เซฟเงียบ ๆ ไม่มีข้อความยืนยัน** — ใส่แล้วเหมือนไม่มีอะไรเกิดขึ้นคือ *ปกติ*
> ไปทดสอบที่หน้า chat เอา อย่านั่งรอ ✓

**Windows: ห้ามใช้ `.cmd` / `.ps1` wrapper** — ใช้ `cli-wrapper.cjs` (npm) หรือ `claude.exe` (native)
ถ้าไม่ตั้ง path จะเจอ `spawn claude ENOENT`

ถ้า node กับ npm อยู่คนละที่: Settings → Environment ใส่ `PATH=/path/to/node/bin`

---

## 6. ⚠️ เปลี่ยน permission mode ก่อนใช้งานจริง

**Claudian default = `permissionMode: "yolo"`** ยืนยันจากโค้ดใน `main.js`:

| บรรทัด | โค้ด | แปลว่า |
|---|---|---|
| 70091 | `if (permissionMode === "yolo") return "bypassPermissions"` | ไม่ถามก่อนทำอะไรเลย |
| 70096 | `options.allowDangerouslySkipPermissions = true` | ปิดด่านขออนุญาตทั้งหมด |
| 80053 | `approvalPolicy: "never", sandbox: "danger-full-access"` | (ฝั่ง Codex) ไม่มี sandbox |

สิ่งที่ต้องเข้าใจ: **vault คือ working directory ไม่ใช่ sandbox** — Bash รันด้วยสิทธิ์ user เต็ม
`cd` ออกนอก vault ได้ แตะไฟล์อะไรก็ได้ที่บัญชีนั้นแตะได้ ไม่มี container กั้น

`safeMode: "acceptEdits"` ที่เห็นใน settings **ไม่ทำงานตอนอยู่ yolo** — บรรทัด 70091 return ก่อน ข้าม safeMode ไปเลย

→ กดปุ่มโหมดที่ขึ้นป้าย **YOLO** ในหน้า chat สลับเป็นโหมดปกติ แล้ว `acceptEdits` จะเริ่มมีผล
(แก้ไฟล์ได้ลื่น แต่คำสั่งอันตรายเด้งถามก่อน)

**ถ้า vault ไม่ใช่ git repo = ไม่มี version control ให้ย้อน** ยิ่งควรออกจาก yolo

---

## 7. Verify

1. ไอคอนหุ่นยนต์ 🤖 **"Open Claudian"** โผล่ที่ ribbon ซ้าย (หรือ `Ctrl+P` → `Claudian: Open chat view`)
2. พิมพ์ `มีไฟล์ .md กี่ไฟล์ใน vault นี้` → ตอบถูก = spawn CLI ได้ + auth ผ่าน + working dir ถูก
   - `spawn ... ENOENT` = path ขั้นที่ 5 ผิด
3. หลังใช้ครั้งแรกต้องมี `vault\.claudian\` (settings/sessions) และ `vault\.claude\` (agents/commands/skills)

**Commands ทั้งหมด** (`Ctrl+P` พิมพ์ `Claudian`):

| คำสั่ง | หมายเหตุ |
|---|---|
| Open chat view | เปิด chat |
| Inline edit | **ไม่มี hotkey มาให้** ตั้งเองที่ Settings → Hotkeys |
| New tab | default สูงสุด 3 แท็บ |
| New session (in current tab) | |

Inline edit: **เลือกข้อความ** = โหมดแก้ (มี word-level diff ให้ดูก่อน accept),
**ไม่เลือก** = แทรกที่ cursor โดยอ่านบริบทรอบ ๆ เอง

---

## 8. เรื่องที่ควรรู้ (ไม่ใช่ขั้นตอนติดตั้ง)

**Skills ตามไปเอง** — `~/.claude/skills` เป็น user-level ใช้ได้ทุก vault ทุกเครื่องที่มีไฟล์นั้น ไม่ต้องตั้งอะไร

**Memory ไม่ตามไป** — Claude Code แยก memory ตาม working directory
(`~/.claude/projects/<เข้ารหัสจาก path>/memory/`) → memory จาก vault นี้กับจากที่อื่นคนละกอง

**อย่ายกทุกอย่างไป CLAUDE.md ระดับ user** — มันโหลดทุก session ทุกโฟลเดอร์
และไม่มีธงเตือนความเก่าแบบ memory (memory จะแปะ *"เก่า N วัน ให้ตรวจก่อนเชื่อ"* ให้)
→ CLAUDE.md ที่เก่าอันตรายกว่า memory ที่เก่า เพราะถูกอ่านเป็นความจริงเสมอ
ใส่เฉพาะกฎที่สากลจริง ๆ สั้น ๆ ห้ามใส่ข้อเท็จจริงที่มีวันหมดอายุ

**Claudian ไม่ได้มาแทน CLI** — vault sidebar ไม่เหมาะกับ debug/test/monorepo
งานโค้ดหนักอยู่ที่ terminal/IDE เหมือนเดิม Claudian ชนะเรื่องงานโน้ต: สรุป เรียบเรียง inline edit

---

## 9. เครื่องบริษัท — เช็คก่อนติดตั้ง

- **นโยบายก่อนเทคนิค**: Claudian ส่ง prompt, เนื้อไฟล์ที่แนบ, และ tool output ออก external API
  ถ้า vault/เครื่องมีข้อมูลบริษัท = ข้อมูลออกนอกองค์กร **ต้องเคลียร์กับ IT ก่อน**
  ยิ่ง yolo (ข้อ 6) ยิ่งต้องคิด — agent สิทธิ์เต็มเครื่องบนเครื่องบริษัทไม่ใช่เรื่องเล็ก
- ติดตั้งลง `%APPDATA%` / vault → **ปกติไม่ต้องใช้ admin** แต่ policy อาจบล็อก npm global install
- มี proxy: Settings → Environment ใส่ `HTTPS_PROXY=...` (subprocess รับ env ต่อ)
- ถ้าองค์กรบล็อก `raw.githubusercontent.com` / `objects.githubusercontent.com` → โหลด release ไม่ได้ ต้องพกไฟล์ไปเอง

---

## อัปเดต / ถอนออก

**อัปเดต**: ไม่มี auto-update — โหลด 3 ไฟล์ทับใหม่ (ข้อ 3) แล้ว reload Obsidian
repo เคลื่อนไหวเร็วมาก ควรเช็ค release เป็นระยะ

**ถอน**: ปิดสวิตช์ใน Community plugins แล้วลบ `vault\.obsidian\plugins\realclaudian\`
ล้างให้หมดก็ลบ `vault\.claudian\` และ `vault\.claude\` ด้วย — ไม่มีอะไรแตะระบบนอก vault
