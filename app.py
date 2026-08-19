from flask import Flask, request, jsonify
import asyncio
import re
from playwright.async_api import async_playwright

app = Flask(__name__)

async def real_bypass(link):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(link, timeout=30000)
            await page.wait_for_load_state("networkidle", timeout=15000)
            content = await page.content()
            token_match = re.search(r'"token":"([^"]+)"', content)
            if token_match:
                await browser.close()
                return {"token": token_match.group(1)}
            await browser.close()
            return {"error": "not_found"}
    except Exception as e:
        return {"error": str(e)}

@app.route('/bypass', methods=['POST'])
def bypass():
    data = request.get_json()
    link = data.get('link')
    if not link:
        return jsonify({"error": "no_link"}), 400
    result = asyncio.run(real_bypass(link))
    return jsonify(result)

@app.route('/')
def home():
    return "Bypass server is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
