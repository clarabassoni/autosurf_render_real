import time
import re
import requests
from datetime import datetime

BASE_URL = "https://antautosurf.com"
EMAIL = "rixxant@libero.it"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0",
    "Accept": "*/*",
    "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": BASE_URL,
    "Connection": "keep-alive"
}

_running = False
_last_run_time = "Mai"

def is_running():
    return _running

def last_run_time():
    return _last_run_time

def get_csrf_token(session):
    try:
        r = session.get(f"{BASE_URL}/index.php?bitcoinwallet={EMAIL}", headers=HEADERS, timeout=20)
    except Exception as e:
        print("❌ Errore GET index:", e)
        return None
    match = re.search(r"csrf_token=([a-z0-9]+)", r.text)
    if match:
        return match.group(1)
    return None

def do_surf_once(session):
    global _last_run_time
    csrf = get_csrf_token(session)
    if not csrf:
        print("❌ CSRF token non trovato.")
        return False

    init_url = f"{BASE_URL}/surf.php?wallet={EMAIL}&key=&time=12&ad_id=&isitbad=0&csrf_token={csrf}"
    try:
        r = session.get(init_url, headers=HEADERS, timeout=20)
    except Exception as e:
        print("❌ Errore init request:", e)
        return False

    text = r.text.strip()
    print("📄 INIT response:", text[:100])
    _last_run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return True

def run_loop():
    global _running
    _running = True
    session = requests.Session()
    while _running:
        do_surf_once(session)
        time.sleep(60)

def stop():
    global _running
    _running = False
