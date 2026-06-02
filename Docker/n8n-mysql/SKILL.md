---
name: n8n-docker-mysql
description: ใช้ skill นี้เมื่อผู้ใช้มีปัญหา n8n MySQL node ต่อ database ไม่ได้ใน Docker environment — trigger เมื่อพูดถึง "n8n mysql ต่อไม่ได้", "ETIMEDOUT", "Couldn't connect", "n8n docker database", "docker subnet conflict" หรือเมื่อ n8n เคยต่อ MySQL ได้แต่ไม่ได้แล้วทั้งที่ service ยังรันอยู่
---

# n8n Docker — MySQL Connection Troubleshoot

Skill นี้ครอบคลุมการวินิจฉัยและแก้ปัญหา n8n MySQL node ที่รันใน Docker ต่อ database ไม่ได้

## Error Map

| Error | สาเหตุ | วิธีแก้ |
|---|---|---|
| `ETIMEDOUT` | Docker subnet ชนกับ IP ของ MySQL server | เปลี่ยน subnet ของ Docker network |
| `ECONNREFUSED` | MySQL service ไม่ได้รัน หรือ port ผิด | เช็ค service + port |
| `Access denied` | username/password ผิด หรือ user ไม่มีสิทธิ์ | เช็ค credential |
| `No testing function found` | n8n ไม่มี built-in test สำหรับ MySQL credential (ปกติ) | ทดสอบผ่าน workflow แทน |

## Step 1 — Diagnose

```powershell
# 1. เช็ค MySQL service
netstat -an | findstr :3306

# 2. ทดสอบจาก host เครื่องนี้
Test-NetConnection -ComputerName <mysql-ip> -Port 3306

# 3. ทดสอบจากใน Docker container
docker exec <n8n-container> sh -c "nc -zv <mysql-ip> 3306 2>&1"
```

**ถ้า host ต่อได้ แต่ container ต่อไม่ได้ → ปัญหา Docker subnet conflict → ไป Step 2**

## Step 2 — ตรวจสอบ Subnet Conflict

```powershell
# ดู network ทั้งหมด
docker network ls

# เช็ค subnet ของแต่ละ network
docker network inspect <network-name> --format "Subnet: {{range .IPAM.Config}}{{.Subnet}}{{end}}"
```

**Conflict เกิดเมื่อ:** subnet ของ Docker network ครอบคลุม IP ของ MySQL server
- ตัวอย่าง: Docker network ใช้ `172.18.0.0/16` และ MySQL อยู่ที่ `172.18.106.100`
- Docker จะ route traffic ไปภายใน network ตัวเองแทนที่จะออกไปหา server จริง

## Step 3 — แก้ไข (เปลี่ยน Subnet)

```powershell
# 1. หา containers ที่อยู่บน network ที่ต้องแก้
docker network inspect <network-name> --format "Containers: {{range .Containers}}{{.Name}} {{end}}"

# 2. หยุด containers เหล่านั้น
docker stop <container1> <container2>

# 3. ถอด containers ออกจาก network
docker network disconnect <network-name> <container1>

# 4. ลบ network เก่า
docker network rm <network-name>

# 5. สร้าง network ใหม่ด้วย subnet ที่ไม่ชน (ใช้ 10.x.x.x ปลอดภัยที่สุด)
docker network create --subnet=10.100.0.0/16 <network-name>

# 6. ต่อ containers กลับเข้า network ใหม่
docker network connect <network-name> <container1>

# 7. Start containers กลับ
docker start <container1> <container2>
```

> **Data ไม่หาย** — การลบ network ไม่กระทบ container หรือ volume เลย

## Step 4 — ยืนยัน

```powershell
# ทดสอบจาก container อีกรอบ — ควรขึ้น "open"
docker exec <n8n-container> sh -c "nc -zv <mysql-ip> 3306 2>&1"
```

จากนั้นทดสอบใน n8n โดยสร้าง workflow → MySQL node → `SELECT 1` → Execute

## ป้องกันบนเครื่องใหม่

ใช้ `docker-compose.yml` กำหนด subnet ตั้งแต่ต้น:

```yaml
networks:
  ai-network:
    driver: bridge
    ipam:
      config:
        - subnet: 10.100.0.0/16
```

## หมายเหตุ

- `172.17.0.0/16` — Docker default bridge (ห้ามใช้ subnet นี้)
- `172.18.0.0/16` — มักถูก Docker สร้าง auto ทำให้ชนกับ company network range
- แนะนำใช้ `10.x.x.x` หรือ `192.168.x.x` สำหรับ custom Docker networks
