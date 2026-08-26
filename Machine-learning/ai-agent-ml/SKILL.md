---
name: ai-agent-ml
description: ใช้ skill นี้เมื่อผู้ใช้ต้องการสร้าง AI agent ที่รัน ML pipeline อัตโนมัติผ่าน Claude API (tool use) trigger เมื่อพูดถึง "สร้าง agent", "agent ทำ ML", "automate ML", "autonomous ML", "agent loop" หรือต้องการระบบที่รับ dataset แล้วให้ผลลัพธ์โมเดลโดยไม่ต้องสั่งทีละขั้น — สำหรับ ML domain knowledge (EDA, preprocessing, training, evaluation) ให้ดูที่ [[machine-learning]]
---

# AI Agent for Machine Learning

Skill นี้ครอบคลุมเฉพาะ **agent architecture** — วิธีสร้าง loop, กำหนด tools, และ orchestrate งาน ML logic ดูที่ [[machine-learning]]

## สถาปัตยกรรม

```
User input (dataset + goal)
        ↓
   Claude (orchestrator)  ←── system prompt กำหนด workflow
        ↓ tool calls
   ┌─────────────────────┐
   │  execute_python     │  ← รัน code ที่ Claude เขียน
   │  read_file          │  ← อ่าน dataset
   │  write_file         │  ← บันทึก model, report
   │  ask_user           │  ← ถามเมื่อ ambiguous เท่านั้น
   └─────────────────────┘
        ↓
   Final report + saved model
```

## 1. Tool Definitions

```python
tools = [
    {
        "name": "execute_python",
        "description": "รัน Python code และ return stdout + stderr",
        "input_schema": {
            "type": "object",
            "properties": {
                "code": {"type": "string"},
                "description": {"type": "string", "description": "อธิบายว่า code นี้ทำอะไร"}
            },
            "required": ["code", "description"]
        }
    },
    {
        "name": "read_file",
        "description": "อ่าน dataset (.csv, .parquet) คืน schema + sample + missing value summary",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"]
        }
    },
    {
        "name": "write_file",
        "description": "บันทึกไฟล์ผลลัพธ์ เช่น report .md หรือ predictions .csv",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "content": {"type": "string"}
            },
            "required": ["path", "content"]
        }
    },
    {
        "name": "ask_user",
        "description": "ถาม user เฉพาะเมื่อ infer ไม่ได้ เช่น target column ที่ไม่ชัดเจน",
        "input_schema": {
            "type": "object",
            "properties": {
                "question": {"type": "string"},
                "options": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["question"]
        }
    }
]
```

## 2. Agent Loop

```python
import anthropic

client = anthropic.Anthropic()

def run_agent(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=tools,
            messages=messages
        )

        if response.stop_reason == "end_turn":
            return next(b.text for b in response.content if hasattr(b, "text"))

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = execute_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result)
                })

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})
```

## 3. Tool Executors

```python
import subprocess, json
import pandas as pd

def execute_tool(name: str, inputs: dict) -> str:
    match name:
        case "execute_python": return run_python(inputs["code"])
        case "read_file":      return read_dataset(inputs["path"])
        case "write_file":     return save_file(inputs["path"], inputs["content"])
        case "ask_user":       return prompt_user(inputs["question"], inputs.get("options"))

def run_python(code: str) -> str:
    result = subprocess.run(["python", "-c", code],
                            capture_output=True, text=True, timeout=120)
    return (result.stdout + result.stderr)[:5000]  # cap เพื่อไม่ให้ context เต็ม

def read_dataset(path: str) -> str:
    df = pd.read_csv(path) if path.endswith(".csv") else pd.read_parquet(path)
    return json.dumps({
        "shape": df.shape,
        "columns": df.dtypes.astype(str).to_dict(),
        "sample": df.head(3).to_dict(),
        "missing": df.isnull().sum().to_dict()
    }, ensure_ascii=False)

def save_file(path: str, content: str) -> str:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"saved: {path}"

def prompt_user(question: str, options: list = None) -> str:
    print(f"\n[Agent]: {question}")
    if options:
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")
    return input("ตอบ: ")
```

## 4. System Prompt

System prompt กำหนด workflow ของ agent — ไม่ใส่ ML knowledge ที่นี่ ให้ Claude ใช้ความรู้ที่มีอยู่แล้ว:

```python
SYSTEM_PROMPT = """คุณคือ ML agent ที่ทำงานอัตโนมัติผ่าน tool calls

workflow ที่ต้องทำตามลำดับ:
1. read_file → ดู schema และ sample
2. ถามด้วย ask_user เฉพาะเมื่อไม่รู้ target column หรือ success criteria
3. execute_python → EDA (distribution, missing, correlation)
4. execute_python → preprocessing + baseline model
5. execute_python → iterate model ถ้า baseline ไม่ถึงเกณฑ์
6. execute_python → evaluation metrics
7. write_file → บันทึก report และ predictions

กฎ:
- อย่าถาม user ในสิ่งที่ infer ได้จากข้อมูล
- set random_state=42 ทุกครั้ง
- return error message ชัดเจนถ้า tool ล้มเหลว อย่า swallow exception"""
```

## การจัดการ Context

tool output สะสมใน messages ทุก turn ถ้าไม่จำกัดจะ overflow:

- cap `execute_python` output ที่ 5000 chars (ทำแล้วใน executor)
- ถ้า EDA มี output ยาว ให้ agent summarize ก่อน pass ต่อ โดยใส่ใน system prompt ว่า "ถ้า output เกิน 2000 chars ให้ summarize เป็น bullet points ก่อน"

## หลักการสำคัญ

**Fail loudly** — executor ต้อง return error จริง ถ้า swallow exception agent จะ hallucinate ผลลัพธ์ที่ไม่เคยเกิดขึ้น

**ถามน้อย** — `ask_user` ควร trigger ไม่เกิน 1-2 ครั้งต่อ session เฉพาะ ambiguity ที่ข้อมูลบอกไม่ได้จริง ๆ

**ML logic ไม่อยู่ที่นี่** — algorithm selection, metric choice, overfitting handling ดูที่ [[machine-learning]]

## ตัวอย่าง

```python
result = run_agent(
    "dataset: /data/churn.csv — สร้างโมเดลทำนาย churn "
    "บันทึก report ที่ /output/report.md"
)
```

agent จะ loop ผ่าน tool calls จนได้ `end_turn` โดยไม่ต้องสั่งทีละขั้น

## ต่อยอด

- เพิ่ม `search_docs` tool ให้ agent ค้นหา scikit-learn API เมื่อต้องการ
- เพิ่ม persistent memory โดยให้ agent `write_file` state ก่อนจบ แล้ว `read_file` เมื่อ resume
