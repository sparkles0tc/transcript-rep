from flask import Flask, Response, abort
import requests
import urllib.parse

app = Flask(__name__)

@app.route('/<path:encoded_url>')
def proxy_discord_html(encoded_url):
    try:
        # Decode the URL (it was encoded in the browser)
        url = urllib.parse.unquote(encoded_url)

        # Only allow Discord CDN links
        if not url.startswith("https://cdn.discordapp.com/attachments/"):
            return abort(403, "Forbidden URL")

        # Fetch the HTML file from Discord
        resp = requests.get(url)

        if resp.status_code != 200:
            return abort(resp.status_code, "Failed to fetch the file")

        # Return the HTML content
        return Response(resp.content, content_type="text/html")

    except Exception as e:
        return abort(500, f"Error: {str(e)}")

# Make sure Flask runs when the file is executed
if __name__ == "__main__":
    app.run(debug=True)
