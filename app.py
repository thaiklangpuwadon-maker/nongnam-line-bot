"""
LINE Bot - น้องน้ำ (Nongnam AI)
ผู้ช่วยกฎหมายและดูแลชาวไทยในเกาหลี
"""

from flask import Flask, request, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
from datetime import datetime
import logging

app = Flask(__name__)

# ตั้งค่า Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ตั้งค่า LINE Bot จาก Environment Variables
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')

if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    logger.warning("⚠️ LINE credentials not found. Bot may not work properly.")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ข้อมูลสำนักงาน
OFFICE_INFO = {
    "name": "Nongnam AI",
    "address": "South Korea",
    "phone": "01055492284",
    "email": "thaiklangpuwadon@gmail.com",
    "hours": "24 ชั่วโมง",
    "line_id": "@932sagnt"
}

# ข้อมูลพื้นฐาน (Knowledge Base)
KNOWLEDGE_BASE = {
    "วีซ่า e-2": {
        "title": "วีซ่า E-2 ต่ออายุ",
        "content": """สวัสดีค่ะ! 👋

📋 **วีซ่า E-2 ต่ออายุ** ทำยังไงค่ะ:

**ขั้นตอน 1: เตรียมเอกสาร**
✓ หนังสือเดินทาง
✓ ใบสมัครวีซ่า (TM.8)
✓ รูปถ่าย 4x6 (2 รูป)
✓ เอกสารการจ้างงาน
✓ ใบเสร็จค่าธรรมเนียม

**ขั้นตอน 2: ไปสำนักงาน Immigration**
📍 ที่อยู่: 39 Nonhyeon-ro, Gangnam-gu, Seoul
📞 เบอร์: 02-3210-0100
⏰ เวลา: 09:00-18:00 (จันทร์-ศุกร์)

**ขั้นตอน 3: ยื่นเอกสาร**
ยื่นให้เจ้าหน้าที่ที่ประตู 2 (Visa Extension)

**ขั้นตอน 4: จ่ายค่าธรรมเนียม**
💰 200,000 วอน (ประมาณ 5,000 บาท)

**ขั้นตอน 5: รับใบเสร็จ**
⏱️ เวลารอ: 3-5 วัน

💡 **เคล็ดลับ:**
• ไปตอนเช้า เพื่อหลีกเลี่ยงคิว
• เตรียมเอกสารครบก่อนไป
• ถ้าไม่เข้าใจ ให้ติดต่อเราค่ะ

---
📞 **ต้องการช่วยเพิ่มเติมไหมค่ะ?**
เบอร์: {phone}
อีเมล: {email}"""
    },
    "นายจ้างไม่จ่ายเงิน": {
        "title": "นายจ้างไม่จ่ายเงิน ทำไง?",
        "content": """สวัสดีค่ะ! 👋

⚠️ **นายจ้างไม่จ่ายเงิน** ทำยังไงค่ะ:

**ขั้นตอน 1: รวบรวมหลักฐาน**
✓ สัญญาจ้าง
✓ ใบเสร็จเงินเดือน
✓ ข้อความ/อีเมล
✓ หลักฐานการทำงาน
✓ รูปถ่ายบ้านจ้าง

**ขั้นตอน 2: ติดต่อเรา**
เราจะช่วยคุณวิเคราะห์สถานการณ์

**ขั้นตอน 3: ยื่นร้องเรียน**
📍 ที่สำนักงาน Labor Office (고용노동부)
📍 ที่อยู่: 1 Cheonggyecheon-ro, Jung-gu, Seoul

**ขั้นตอน 4: ติดตามคดี**
เราจะติดตามให้คุณ

---
⚠️ **สิ่งสำคัญ:**
• อย่าลาออกก่อน
• เก็บหลักฐาน
• ติดต่อเราเร็ว
• ไม่มีค่าใช้จ่าย

---
📞 **ติดต่อเราเลยค่ะ!**
เบอร์: {phone}
อีเมล: {email}"""
    },
    "หมอที่ไหน": {
        "title": "หมอที่ไหน?",
        "content": """สวัสดีค่ะ! 👋

🏥 **โรงพยาบาลใหญ่ในเกาหลี:**

**1. Seoul National University Hospital**
📍 ที่อยู่: 101 Daehak-ro, Jongno-gu, Seoul
📞 เบอร์: 02-2072-2114
🚇 สถานี: Daehak-ro Station

**2. Asan Medical Center**
📍 ที่อยู่: 88 Olympic-ro 43-gil, Songpa-gu, Seoul
📞 เบอร์: 02-3010-3114
🚇 สถานี: Olympic Park Station

**3. Samsung Medical Center**
📍 ที่อยู่: 81 Irwon-ro, Gangnam-gu, Seoul
📞 เบอร์: 02-3410-0114
🚇 สถานี: Samseong Station

**4. Severance Hospital**
📍 ที่อยู่: 50-1 Yonsei-ro, Seodaemun-gu, Seoul
📞 เบอร์: 02-2228-5800
🚇 สถานี: Sinchon Station

---
💡 **เคล็ดลับ:**
• โทรก่อนไปเพื่อจองคิว
• นำหนังสือเดินทาง
• ถามเรื่องประกันสุขภาพ
• ถ้าไม่พูดเกาหลี ให้ติดต่อเรา

---
📞 **ต้องการล่ามไหมค่ะ?**
เบอร์: {phone}
อีเมล: {email}"""
    },
    "ที่พัก": {
        "title": "หาที่พักในเกาหลี",
        "content": """สวัสดีค่ะ! 👋

🏠 **หาที่พักในเกาหลี:**

**เว็บไซต์หลัก:**
• Naver: www.naver.com (ค้นหา "원룸" = วันรูม)
• Daangn: www.daangn.com (ตลาดโลก)
• Zigbang: www.zigbang.com (เว็บเฉพาะที่พัก)

**ราคาโดยทั่วไป:**
• วันรูม (1 ห้อง): 300,000 - 600,000 วอน
• ห้องแบ่ง: 200,000 - 400,000 วอน
• อพาร์ท: 500,000 - 1,500,000 วอน

**สิ่งที่ต้องรู้:**
• ค่าเดือนแรก + ค่ามัดจำ (보증금)
• ค่าไฟ/น้ำ ประมาณ 50,000-100,000 วอน
• ต้องมีเลขประจำตัวเกาหลี (ARC)

---
📞 **ต้องการช่วยหาที่พักไหมค่ะ?**
เบอร์: {phone}
อีเมล: {email}"""
    },
    "ธนาคาร": {
        "title": "เปิดบัญชีธนาคารในเกาหลี",
        "content": """สวัสดีค่ะ! 👋

🏦 **เปิดบัญชีธนาคารในเกาหลี:**

**ธนาคารหลัก:**
• KB Kookmin Bank
• Shinhan Bank
• Woori Bank
• Hana Bank

**เอกสารที่ต้อง:**
✓ หนังสือเดินทาง
✓ เลขประจำตัวเกาหลี (ARC)
✓ ใบสมัครงาน
✓ ที่อยู่ในเกาหลี

**ขั้นตอน:**
1. ไปสาขาธนาคาร
2. บอกต้องการเปิดบัญชี
3. เตรียมเอกสาร
4. ลงนาม
5. รับบัตรเดบิต

**ค่าธรรมเนียม:**
• ฟรี (ไม่มีค่าใช้จ่าย)

---
💡 **เคล็ดลับ:**
• เปิดบัญชีเร็ว ๆ เพื่อรับเงินเดือน
• ถ้าไม่พูดเกาหลี ให้ติดต่อเรา

---
📞 **ต้องการช่วยไหมค่ะ?**
เบอร์: {phone}
อีเมล: {email}"""
    }
}

def get_response(question):
    """ค้นหาคำตอบจาก Knowledge Base"""
    question_lower = question.lower()
    
    # ค้นหาคำสำคัญ
    for key, value in KNOWLEDGE_BASE.items():
        if key in question_lower:
            content = value['content'].format(
                phone=OFFICE_INFO['phone'],
                email=OFFICE_INFO['email']
            )
            return content
    
    # ถ้าไม่เจอ ให้ตอบแบบทั่วไป
    return get_default_response()

def get_default_response():
    """ตอบแบบทั่วไป"""
    response = f"""สวัสดีค่ะ! 👋

ผมชื่อน้องน้ำค่ะ ยินดีที่ได้ช่วยคุณค่ะ 💕

**ผมสามารถช่วยเรื่องนี้ได้ค่ะ:**
✅ วีซ่า (E-2, D-2, F-2)
✅ ปัญหากฎหมาย
✅ สุขภาพและโรงพยาบาล
✅ ที่พักและความเป็นอยู่
✅ ธนาคารและการเงิน

**ลองถามผมสิค่ะ เช่น:**
• "วีซ่า E-2 ต่ออายุยังไง?"
• "นายจ้างไม่จ่ายเงิน ทำไง?"
• "หมอที่ไหน?"
• "ที่พัก"
• "ธนาคาร"

---
📞 **ต้องการติดต่อทีมงาน?**
เบอร์: {phone}
อีเมล: {email}
LINE: {line_id}

เวลาทำการ: {hours}""".format(
        phone=OFFICE_INFO['phone'],
        email=OFFICE_INFO['email'],
        line_id=OFFICE_INFO['line_id'],
        hours=OFFICE_INFO['hours']
    )
    return response

@app.route("/callback", methods=['POST'])
def callback():
    """รับข้อมูลจาก LINE"""
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    logger.info(f"Request body: {body}")
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("Invalid signature")
        return 'Invalid signature', 400
    
    return 'OK', 200

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """จัดการข้อความจากผู้ใช้"""
    user_message = event.message.text
    user_id = event.source.user_id
    
    logger.info(f"User {user_id} sent: {user_message}")
    
    # ค้นหาคำตอบ
    response = get_response(user_message)
    
    # ส่งคำตอบ
    try:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response)
        )
    except Exception as e:
        logger.error(f"Error sending message: {e}")

@app.route("/health", methods=['GET'])
def health():
    """ตรวจสอบสถานะ Bot"""
    return jsonify({
        "status": "healthy",
        "bot_name": "น้องน้ำ",
        "office": OFFICE_INFO["name"],
        "timestamp": datetime.now().isoformat()
    })

@app.route("/", methods=['GET'])
def index():
    """หน้าแรก"""
    return jsonify({
        "message": "น้องน้ำ LINE Bot is running!",
        "bot_name": "น้องน้ำ",
        "office": OFFICE_INFO["name"],
        "health_check": "/health"
    })

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
