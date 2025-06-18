from flask import Flask, Response, abort
import requests
import urllib.parse
import os

app = Flask(__name__)

@app.route('/')
def home():
    return ":white_check_mark: CDN Viewer is Running! Use an encoded Discord CDN URL after the slash."

@app.route('/<path:encoded_url>')
def proxy_discord_html(encoded_url):
    try:
        # Decode the URL-encoded Discord CDN link
        url = urllib.parse.unquote(encoded_url)

        # Security check: only allow Discord CDN attachment URLs
        if not url.startswith("https://cdn.discordapp.com/attachments/"):
            return abort(403, "Forbidden: Only Discord CDN URLs allowed.")

        # Fetch the content from Discord CDN
        resp = requests.get(url)

        if resp.status_code != 200:
            return abort(resp.status_code, "Failed to fetch the file from Discord.")

        # Return the HTML content with correct content type
        return Response(resp.content, content_type="text/html")

    except Exception as e:
        return abort(500, f"Server error: {str(e)}")

if __name__ == "__main__":
    # Get the PORT environment variable Render/Replit sets, default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
