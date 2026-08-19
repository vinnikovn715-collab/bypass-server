from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

def real_bypass(link):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive"
        }
        response = requests.get(link, headers=headers, timeout=15)
        html = response.text
        
        if "expired" in html.lower() or "invalid" in html.lower():
            return {"error": "expired"}
        
        token_match = re.search(r'"token":"([^"]+)"', html)
        if token_match:
            return {"token": token_match.group(1)}
        
        redirect_match = re.search(r'window\.location\.href\s*=\s*"([^"]+)"', html)
        if redirect_match:
            d_match = re.search(r'd=([^&]+)', redirect_match.group(1))
            if d_match:
                return {"token": d_match.group(1)}
        
        hidden_match = re.search(r'<input[^>]+name="token"[^>]+value="([^"]+)"', html)
        if hidden_match:
            return {"token": hidden_match.group(1)}
        
        if "captcha" in html.lower():
            return {"error": "captcha"}
            
        return {"error": "not_found"}
    except Exception as e:
        return {"error": str(e)}

@app.route('/bypass', methods=['POST'])
def bypass():
    data = request.get_json()
    link = data.get('link')
    if not link:
        return jsonify({"error": "no_link"}), 400
    result = real_bypass(link)
    return jsonify(result)

@app.route('/')
def home():
    return "Bypass server is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
