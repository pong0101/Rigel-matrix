# Rigel Matrix
### ระบบบริษัท AI สำหรับ Raspberry Pi

Rigel Matrix คือระบบ Multi-Agent AI Operating Company ที่ออกแบบมาเพื่อทำงานบน Raspberry Pi โดยเฉพาะ

ระบบนี้จำลองการทำงานของบริษัท AI ที่มีหลาย Agent ทำงานร่วมกันผ่านห้องประชุมกลางบนหน้าเว็บ เพื่อวิเคราะห์งาน ประมวลผล และบันทึกความรู้

---

## แนวคิดของโปรเจกต์

Rigel Matrix ไม่ใช่ chatbot ธรรมดา แต่เป็นศูนย์บัญชาการ AI ที่แบ่งบทบาทชัดเจนเหมือนองค์กรจริง

แต่ละ Agent มีหน้าที่เฉพาะ และร่วมกันประชุม วิเคราะห์ ตัดสินใจ และบันทึกข้อมูล

---

## Agent ภายในระบบ

### RM-CEO
ผู้บริหารการประชุม

### RM-SYS
ตรวจสอบสถานะระบบ Raspberry Pi

### RM-ANL
วิเคราะห์ปัญหาและสรุปผล

### RM-DEV
เสนอแนวทางพัฒนาและแก้ไขระบบ

### RM-MEM
จัดเก็บประวัติการประชุมและ task history

---

## ฟีเจอร์หลัก

- Multi-Agent Boardroom
- Raspberry Pi System Monitoring
- Persistent JSON Memory
- Provider Settings แบบละเอียด
- Web Dashboard ห้องประชุม AI
- รองรับเปลี่ยน Provider ได้

---

## Hardware ที่รองรับ

- Raspberry Pi Zero 2 W
- Raspberry Pi 4
- Raspberry Pi 5
- Linux Mini PC

---

## ติดตั้ง

```bash
git clone https://github.com/pong0101/Rigel-matrix.git
cd Rigel-matrix
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## รัน Web Dashboard

```bash
uvicorn web:app --host 0.0.0.0 --port 8000
```

เปิดผ่านเบราว์เซอร์:

```text
http://IP-RASPBERRYPI:8000
```

---

## Provider Settings

ตั้งค่าผ่านหน้าเว็บได้ครบ:

- Provider
- Base URL
- Model
- Temperature
- Max Tokens
- Timeout
- API Key

ค่าเริ่มต้นใช้ DeepSeek

---

## Memory System

เก็บข้อมูลไว้ที่

`memory/state.json`

เก็บ:
- เวลา
- Task
- ผลลัพธ์จาก Agent

---

## เป้าหมายในอนาคต

### v0.4
เชื่อม AI API จริง

### v0.5
Agent Streaming Discussion

### v1.0
Autonomous AI Company

---

## ปรัชญาของ Rigel Matrix

Rigel Matrix ถูกสร้างขึ้นเพื่อเป็นบริษัท AI ขนาดเล็กที่ทำงานอยู่บน Raspberry Pi
