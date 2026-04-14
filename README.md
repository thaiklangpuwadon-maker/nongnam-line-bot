# 🤖 น้องน้ำ LINE Bot

ผู้ช่วยกฎหมายและดูแลชาวไทยในเกาหลี

## 📋 ข้อมูล

- **ชื่อ Bot:** น้องน้ำ
- **LINE OA ID:** @932sagnt
- **สำนักงาน:** Nongnam AI
- **ที่อยู่:** South Korea
- **เบอร์โทร:** 01055492284
- **อีเมล:** thaiklangpuwadon@gmail.com
- **เวลาทำการ:** 24 ชั่วโมง

## 🎯 ฟีเจอร์

- ✅ ตอบคำถามเกี่ยวกับวีซ่า
- ✅ ช่วยเรื่องปัญหากฎหมาย
- ✅ ให้ข้อมูลสุขภาพและโรงพยาบาล
- ✅ ช่วยเรื่องที่พักและความเป็นอยู่
- ✅ ให้ข้อมูลธนาคาร
- ✅ ปุ่มติดต่อทีมงาน

## 🚀 วิธีการใช้

### ทดสอบในเครื่อง

```bash
# ติดตั้ง dependencies
pip install -r requirements.txt

# ตั้ง Environment Variables
export LINE_CHANNEL_ACCESS_TOKEN="your-token"
export LINE_CHANNEL_SECRET="your-secret"

# รัน Bot
python app.py
```

### Deploy ไปที่ Render

1. สร้าง GitHub Repository
2. Push Code ไปที่ GitHub
3. ไปที่ Render.com
4. สร้าง New Web Service
5. เชื่อมต่อ GitHub Repository
6. ตั้ง Environment Variables:
   - `LINE_CHANNEL_ACCESS_TOKEN`
   - `LINE_CHANNEL_SECRET`
7. Deploy

## 🔧 ตั้งค่า LINE Messaging API

### ขั้นตอน 1: สร้าง Channel

1. ไปที่ https://developers.line.biz/
2. คลิก "Create a new channel"
3. เลือก "Messaging API"
4. กรอกข้อมูล
5. คลิก "Create"

### ขั้นตอน 2: ได้รับ Credentials

1. ไปที่ "Channel settings"
2. ค้นหา "Messaging API"
3. Copy "Channel access token"
4. Copy "Channel secret"

### ขั้นตอน 3: ตั้ง Webhook URL

1. ไปที่ "Messaging API" → "Channel settings"
2. ใส่ Webhook URL: `https://your-app.onrender.com/callback`
3. คลิก "Verify"
4. เปิด "Use webhook"

### ขั้นตอน 4: เชื่อมต่อกับ Official Account

1. ไปที่ LINE Business Center
2. เลือก Official Account (@932sagnt)
3. ไปที่ "Settings" → "Linked Services"
4. เลือก "Messaging API"
5. เชื่อมต่อ

## 🧪 ทดสอบ Bot

### ทดสอบผ่าน LINE

1. เพิ่ม @932sagnt เป็นเพื่อน
2. พิมพ์ข้อความ:
   ```
   วีซ่า E-2 ต่ออายุยังไง?
   ```
3. Bot ควรตอบกลับ

### ทดสอบ Health Check

```bash
curl https://your-app.onrender.com/health
```

ควรได้:
```json
{
  "status": "healthy",
  "bot_name": "น้องน้ำ",
  "office": "Nongnam AI",
  "timestamp": "2024-01-15T10:30:00"
}
```

## 📁 โครงสร้าง

```
nongnam-line-bot/
├── app.py              # Bot Code หลัก
├── requirements.txt    # Dependencies
├── Procfile           # ตั้งค่า Render
├── .gitignore         # Git ignore
└── README.md          # ไฟล์นี้
```

## 📞 ติดต่อ

- 📧 อีเมล: thaiklangpuwadon@gmail.com
- 📱 เบอร์: 01055492284
- 💬 LINE: @932sagnt

## 📚 ข้อมูลเพิ่มเติม

- [LINE Developers](https://developers.line.biz/)
- [LINE Bot SDK](https://github.com/line/line-bot-sdk-python)
- [Render.com](https://render.com/)
- [Flask](https://flask.palletsprojects.com/)

---

**สร้างเมื่อ:** 2024-01-15
**เวอร์ชัน:** 1.0.0
**สถานะ:** Ready for Deployment
