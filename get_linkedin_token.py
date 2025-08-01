import webbrowser
import http.server
import socketserver
import requests
import urllib.parse
import os

# ENV or hardcoded values
CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID") or "your_client_id"
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET") or "your_client_secret"
REDIRECT_URI = "http://localhost:8000"
PORT = 8000

# Step 1: Build auth URL
auth_url = (
    "https://www.linkedin.com/oauth/v2/authorization?"
    + urllib.parse.urlencode({
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "w_member_social"
    })
)

# Step 2: Handle the callback and extract code
class LinkedInHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        code = params.get("code")
        if code:
            code = code[0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Authorization successful. You can close this window.")
            print(f"\n✅ Authorization code: {code}")
            # Step 3: Exchange code for token
            token_url = "https://www.linkedin.com/oauth/v2/accessToken"
            data = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
            }
            r = requests.post(token_url, data=data)
            print(f"\n🎫 Access Token Response:\n{r.json()}")
            os._exit(0)  # Exit after done

# Step 4: Launch local server and open browser
print("🌐 Opening browser for LinkedIn authorization...")
webbrowser.open(auth_url)

with socketserver.TCPServer(("", PORT), LinkedInHandler) as httpd:
    print(f"🚪 Listening at http://localhost:{PORT}")
    httpd.serve_forever()
