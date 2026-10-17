import requests, time, re, json, os, threading
from flask import Flask
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is running!"
BOT_TOKEN = "8843607211:AAESIC0aR4bN7ghvWYd_PNTK_xB4gUzeeRg"
CHAT_ID = "5386518430"
AFFILIATE = "C1000094L"
PRODUCTS = ["N70158921V","N70158922V","N70202441V","N70202442V","N70202444V","N70202445V","N70202446V","N70202447V","N70213059V","N70213061V","N70213062V","N70214271V","N70214273V","N70214274V","N70214275V","N70214276V","N70214277V","N70214283V","N70214292V","N70221570V","N70221571V","N70267680V","N70267681V","N70275701V","N70275924V","N70357049V","N70357050V","N70357051V","N70357052V","N70357053V","N70357054V","N70371795V","N70371796V","N70377905V","N70377906V","N70377908V","N70379504V","N70395890V","N70395891V","N70395892V","N70397000V","N70400926V","N70405458V","N70405459V","N70405460V","N70405461V","N71466755V"]
FILE = "prices.json"
def send_telegram(t):
 try: requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id":CHAT_ID,"text":t}, timeout=20)
 except: pass
def get_price(code):
 try:
  r=requests.get(f"https://www.noon.com/egypt-ar/{code}/p/", headers={"User-Agent":"Mozilla/5.0"}, timeout=60)
  m=re.search(r'"sale_price":\s*(\d+)', r.text)
  if m: return int(m.group(1))
 except: pass
 return None
def bot_loop():
 if os.path.exists(FILE):
  with open(FILE,"r") as f: lowest=json.load(f)
 else: lowest={}
 if not lowest:
  for c in PRODUCTS:
   p=get_price(c)
   if p: lowest[c]=p; open(FILE,"w").write(json.dumps(lowest))
   time.sleep(4)
  send_telegram(f"✅ البوت اشتغل 24 ساعة! براقب {len(lowest)} منتج")
 while True:
  for c in PRODUCTS:
   new=get_price(c)
   if not new: time.sleep(5); continue
   old=lowest.get(c,new)
   if new<old:
    link=f"https://www.noon.com/egypt-ar/{c}/p/?utm_source={AFFILIATE}"
    send_telegram(f"🔥 سعر نزل!\n{c}\nمن {old}ج لـ {new}ج\n{link}")
    lowest[c]=new; open(FILE,"w").write(json.dumps(lowest))
   time.sleep(8)
  time.sleep(120)
threading.Thread(target=bot_loop, daemon=True).start()
if __name__=="__main__": app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
