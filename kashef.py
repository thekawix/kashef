#!/usr/bin/python

import json
import requests
import time
import os
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from sys import stderr
import webbrowser
from datetime import datetime

R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
P = '\033[95m'
C = '\033[96m'
W = '\033[97m'
N = '\033[0m'
BL = '\033[90m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    stderr.writelines(f"""
{C}        ██╗  ██╗ █████╗ ███████╗██╗  ██╗███████╗███████╗
{C}        ██║ ██╔╝██╔══██╗██╔════╝██║  ██║██╔════╝██╔════╝
{C}        █████╔╝ ███████║███████╗███████║█████╗  █████╗  
{C}        ██╔═██╗ ██╔══██║╚════██║██╔══██║██╔══╝  ██╔══╝  
{C}        ██║  ██╗██║  ██║███████║██║  ██║██║     ██║     
{C}        ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝     
{Y}   ╔═══════════════════════════════════════════════════════════╗
{Y}   ║  {G}🔍 KASHEF {Y}- {W}Advanced Tracking & Intelligence Tool  {Y}║
{Y}   ║  {C}⚡ Developed by {W}KAWIX {C}⚡                         {Y}║
{Y}   ╚═══════════════════════════════════════════════════════════╝
{P}                🌐 TRACK • DISCOVER • ANALYZE 🌐
{B}                📡 {W}Location • IP • Phone • Social {B}📡
    """)

def show_loading(seconds=1):
    chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    for i in range(seconds * 10):
        stderr.write(f'\r{G}[{chars[i % len(chars)]}] {W}Processing...{N}')
        time.sleep(0.1)
    stderr.write('\r' + ' ' * 30 + '\r')

def print_header(title):
    print(f"\n{Y}╔{'═' * 50}╗")
    print(f"{Y}║ {C}► {W}{title}{' ' * (50 - len(title) - 4)}{Y}║")
    print(f"{Y}╚{'═' * 50}╝{N}")

def ip_tracker():
    print_header("IP ADDRESS TRACKER")
    ip = input(f"{W}\n  📍 Enter Target IP : {G}")
    
    if ip.lower() == 'me':
        ip = requests.get('https://api.ipify.org/').text
    
    print(f"\n{G}  ╔{'═' * 55}╗")
    print(f"{G}  ║{W}  📊 IP INFORMATION RESULT {G}║")
    print(f"{G}  ╚{'═' * 55}╝{N}")
    
    try:
        show_loading(2)
        req_api = requests.get(f"http://ipwho.is/{ip}", timeout=10)
        data = json.loads(req_api.text)
        
        info = [
            ("🎯 IP Target", ip),
            ("📁 Type", data.get("type", "N/A")),
            ("🌍 Country", data.get("country", "N/A")),
            ("🏷️ Country Code", data.get("country_code", "N/A")),
            ("🏙️ City", data.get("city", "N/A")),
            ("🌎 Continent", data.get("continent", "N/A")),
            ("📍 Region", data.get("region", "N/A")),
            ("📌 Latitude", data.get("latitude", "N/A")),
            ("📌 Longitude", data.get("longitude", "N/A")),
            ("🗺️ EU Member", data.get("is_eu", "N/A")),
            ("📮 Postal", data.get("postal", "N/A")),
            ("📞 Calling Code", data.get("calling_code", "N/A")),
            ("🏛️ Capital", data.get("capital", "N/A")),
            ("🔗 Borders", data.get("borders", "N/A")),
            ("🏁 Flag", data.get("flag", {}).get("emoji", "N/A")),
            ("🔢 ASN", data.get("connection", {}).get("asn", "N/A")),
            ("🏢 ORG", data.get("connection", {}).get("org", "N/A")),
            ("📡 ISP", data.get("connection", {}).get("isp", "N/A")),
            ("🌐 Domain", data.get("connection", {}).get("domain", "N/A")),
            ("🕐 Timezone", data.get("timezone", {}).get("id", "N/A")),
        ]
        
        for label, value in info:
            print(f"{W}  ├─ {label} : {G}{value}")
        
        lat = data.get('latitude', 0)
        lon = data.get('longitude', 0)
        maps_url = f"https://www.google.com/maps/@{lat},{lon},12z"
        print(f"{W}  ├─ 🗺️ Google Maps : {C}{maps_url}")
        print(f"{W}  └─ 🕐 Current Time : {G}{data.get('timezone', {}).get('current_time', 'N/A')}")
        print(f"{G}  ╚{'═' * 55}╝{N}")
        
        open_map = input(f"\n{W}  🗺️ Open in Google Maps? (y/n) : {G}")
        if open_map.lower() == 'y':
            webbrowser.open(maps_url)
            
    except Exception as e:
        print(f"{R}  ✖ Error: {e}{N}")

def phone_tracker():
    print_header("PHONE NUMBER TRACKER")
    phone = input(f"{W}\n  📱 Enter Phone Number {G}Ex [+628123456789] : {W}")
    
    try:
        show_loading(2)
        parsed = phonenumbers.parse(phone, "ID")
        
        print(f"\n{G}  ╔{'═' * 55}╗")
        print(f"{G}  ║{W}  📱 PHONE INFORMATION RESULT {G}║")
        print(f"{G}  ╚{'═' * 55}╝{N}")
        
        info = [
            ("📍 Location", geocoder.description_for_number(parsed, "id")),
            ("🏷️ Region Code", phonenumbers.region_code_for_number(parsed)),
            ("🕐 Timezone", ', '.join(timezone.time_zones_for_number(parsed))),
            ("📡 Operator", carrier.name_for_number(parsed, "en")),
            ("✅ Valid", "✓ Yes" if phonenumbers.is_valid_number(parsed) else "✗ No"),
            ("🔢 Possible", "✓ Yes" if phonenumbers.is_possible_number(parsed) else "✗ No"),
            ("🌐 International", phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)),
            ("📱 Mobile Format", phonenumbers.format_number_for_mobile_dialing(parsed, "ID", with_formatting=True)),
            ("🔢 E.164", phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)),
            ("🌍 Country Code", parsed.country_code),
            ("📞 Local Number", parsed.national_number),
        ]
        
        num_type = phonenumbers.number_type(parsed)
        type_map = {
            phonenumbers.PhoneNumberType.MOBILE: "📱 Mobile",
            phonenumbers.PhoneNumberType.FIXED_LINE: "☎️ Fixed Line",
            phonenumbers.PhoneNumberType.VOIP: "📶 VoIP",
            phonenumbers.PhoneNumberType.PAGER: "📟 Pager",
        }
        info.append(("📌 Type", type_map.get(num_type, "❓ Unknown")))
        
        for label, value in info:
            print(f"{W}  ├─ {label} : {G}{value}")
        print(f"{G}  ╚{'═' * 55}╝{N}")
        
    except Exception as e:
        print(f"{R}  ✖ Invalid phone number! {N}")

def username_tracker():
    print_header("USERNAME TRACKER")
    username = input(f"{W}\n  👤 Enter Username : {G}")
    
    social_media = [
        {"url": "https://www.facebook.com/{}", "name": "Facebook", "icon": "📘"},
        {"url": "https://www.twitter.com/{}", "name": "Twitter", "icon": "🐦"},
        {"url": "https://www.instagram.com/{}", "name": "Instagram", "icon": "📸"},
        {"url": "https://www.linkedin.com/in/{}", "name": "LinkedIn", "icon": "💼"},
        {"url": "https://www.github.com/{}", "name": "GitHub", "icon": "🐙"},
        {"url": "https://www.pinterest.com/{}", "name": "Pinterest", "icon": "📌"},
        {"url": "https://www.tumblr.com/{}", "name": "Tumblr", "icon": "📓"},
        {"url": "https://www.youtube.com/{}", "name": "YouTube", "icon": "📺"},
        {"url": "https://soundcloud.com/{}", "name": "SoundCloud", "icon": "🎵"},
        {"url": "https://www.tiktok.com/@{}", "name": "TikTok", "icon": "🎶"},
        {"url": "https://www.behance.net/{}", "name": "Behance", "icon": "🎨"},
        {"url": "https://www.medium.com/@{}", "name": "Medium", "icon": "✍️"},
        {"url": "https://www.quora.com/profile/{}", "name": "Quora", "icon": "❓"},
        {"url": "https://www.twitch.tv/{}", "name": "Twitch", "icon": "🎮"},
        {"url": "https://www.dribbble.com/{}", "name": "Dribbble", "icon": "🏀"},
        {"url": "https://www.producthunt.com/@{}", "name": "Product Hunt", "icon": "🚀"},
        {"url": "https://www.telegram.me/{}", "name": "Telegram", "icon": "✈️"},
        {"url": "https://www.reddit.com/user/{}", "name": "Reddit", "icon": "🤖"},
        {"url": "https://www.snapchat.com/add/{}", "name": "Snapchat", "icon": "👻"},
        {"url": "https://www.tiktok.com/@{}", "name": "TikTok", "icon": "🎵"},
    ]
    
    print(f"\n{G}  ╔{'═' * 55}╗")
    print(f"{G}  ║{W}  👤 USERNAME SEARCH RESULT {G}║")
    print(f"{G}  ╚{'═' * 55}╝{N}")
    
    found = 0
    for site in social_media:
        try:
            url = site['url'].format(username)
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"{G}  ✓ {site['icon']} {site['name']} : {C}{url}")
                found += 1
            else:
                print(f"{BL}  ✗ {site['icon']} {site['name']} : Not Found{N}")
        except:
            print(f"{BL}  ✗ {site['icon']} {site['name']} : Error{N}")
        time.sleep(0.1)
    
    print(f"{G}  ╚{'═' * 55}╝{N}")
    print(f"\n{W}  📊 Total Found : {G}{found}{N}")

def show_my_ip():
    print_header("YOUR IP ADDRESS")
    try:
        response = requests.get('https://api.ipify.org/')
        my_ip = response.text
        
        print(f"\n{G}  ╔{'═' * 55}╗")
        print(f"{G}  ║{W}  🌐 YOUR PUBLIC IP {G}║")
        print(f"{G}  ╚{'═' * 55}╝{N}")
        print(f"\n{W}  🎯 Your IP : {G}{my_ip}")
        
        req = requests.get(f"http://ipwho.is/{my_ip}")
        data = json.loads(req.text)
        print(f"  📍 Location : {G}{data.get('city', 'N/A')}, {data.get('country', 'N/A')}")
        print(f"  📡 ISP : {G}{data.get('connection', {}).get('isp', 'N/A')}")
        print(f"{G}  ╚{'═' * 55}╝{N}")
        
    except Exception as e:
        print(f"{R}  ✖ Error: {e}{N}")

def about():
    print_header("ABOUT KASHEF")
    print(f"""
{C}  ╔═══════════════════════════════════════════════════════════╗
{C}  ║{W}  🔍 KASHEF - Advanced Tracking & Intelligence Tool {C}║
{C}  ║{W}  ⚡ Version : 2.0                                   {C}║
{C}  ║{W}  👤 Author  : {G}KAWIX                                {C}║
{C}  ║{W}  📅 Date    : {G}{datetime.now().strftime('%Y-%m-%d')}{C}              ║
{C}  ║                                                       ║
{C}  ║{W}  Features :                                        {C}║
{C}  ║{W}    • IP Address Tracker                           {C}║
{C}  ║{W}    • Phone Number Tracker                        {C}║
{C}  ║{W}    • Username Finder (20+ Platforms)             {C}║
{C}  ║{W}    • Geo Location & Maps                        {C}║
{C}  ║{W}    • ISP & Carrier Information                  {C}║
{C}  ║                                                       ║
{C}  ║{Y}  📚 For Educational Purposes Only!                 {C}║
{C}  ║{Y}  🔒 Respect Privacy & Laws                        {C}║
{C}  ╚═══════════════════════════════════════════════════════════╝{N}
    """)

menu_options = [
    {'num': 1, 'icon': '🌐', 'text': 'IP Tracker', 'func': ip_tracker},
    {'num': 2, 'icon': '📡', 'text': 'Show My IP', 'func': show_my_ip},
    {'num': 3, 'icon': '📱', 'text': 'Phone Number Tracker', 'func': phone_tracker},
    {'num': 4, 'icon': '👤', 'text': 'Username Tracker', 'func': username_tracker},
    {'num': 5, 'icon': 'ℹ️', 'text': 'About Kashef', 'func': about},
    {'num': 0, 'icon': '🚪', 'text': 'Exit', 'func': exit},
]

def show_menu():
    print(f"\n{Y}  ╔{'═' * 55}╗")
    print(f"{Y}  ║{W}  🎯 MAIN MENU {Y}║")
    print(f"{Y}  ╚{'═' * 55}╝{N}")
    
    for opt in menu_options:
        print(f"{W}    {opt['icon']} [{opt['num']}] {G}{opt['text']}")
    
    print(f"\n{BL}  ╔{'═' * 55}╗")
    print(f"{BL}  ║{W}  💡 Tip : {BL}Enter number to select option {BL}║")
    print(f"{BL}  ╚{'═' * 55}╝{N}")

def main():
    while True:
        print_banner()
        show_menu()
        
        try:
            choice = input(f"\n{W}  ➜ Select Option : {G}")
            
            if choice == '0':
                print(f"\n{C}  👋 Goodbye! See you next time!{N}")
                break
            
            selected = None
            for opt in menu_options:
                if str(opt['num']) == choice:
                    selected = opt
                    break
            
            if selected:
                selected['func']()
                input(f"\n{W}  Press {G}Enter {W}to continue...{N}")
            else:
                print(f"{R}  ✖ Invalid option!{N}")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print(f"\n{C}  👋 Goodbye!{N}")
            break
        except Exception as e:
            print(f"{R}  ✖ Error: {e}{N}")
            time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C}  👋 Exiting...{N}")
